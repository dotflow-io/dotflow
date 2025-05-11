"""Workflow module"""

import threading
import warnings
import platform

from datetime import datetime
from multiprocessing import Process, Queue

from uuid import UUID, uuid4
from typing import Callable, Dict, List

from dotflow.abc.flow import Flow
from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.types import TypeExecution, TypeStatus
from dotflow.core.task import Task
from dotflow.utils import basic_callback


def is_darwin() -> bool:
    """Is Darwin"""
    return platform.system() == "Darwin"


def grouper(tasks: List[Task]) -> Dict[str, List[Task]]:
    """Grouper"""
    groups = {}
    for task in tasks:
        if not groups.get(task.group_name):
            groups[task.group_name] = []
        groups[task.group_name].append(task)

    return groups


class Manager:
    """
    Import:
        You can import the **Manager** class with:

            from dotflow.core.workflow import Manager

    Example:
        `class` dotflow.core.workflow.Manager

            workflow = Manager(
                tasks=[tasks],
                on_success=basic_callback,
                on_failure=basic_callback,
                keep_going=True
            )

    Args:
        tasks (List[Task]):
            A list containing objects of type Task.

        on_success (Callable):
            Success function to be executed after the completion of the entire
            workflow. It's essentially a callback for successful scenarios.

        on_failure (Callable):
            Failure function to be executed after the completion of the entire
            workflow. It's essentially a callback for error scenarios

        mode (TypeExecution):
            Parameter that defines the execution mode of the workflow. Currently,
            there are options to execute in **sequential**, **background**, or **parallel** mode.
            The sequential mode is used by default.


        keep_going (bool):
            A parameter that receives a boolean object with the purpose of continuing
            or not the execution of the workflow in case of an error during the
            execution of a task. If it is **true**, the execution will continue;
            if it is **False**, the workflow will stop.

        workflow_id (UUID): Workflow ID.

    Attributes:
        on_success (Callable):

        on_failure (Callable):

        workflow_id (UUID):

        started (datetime):
    """

    def __init__(
        self,
        tasks: List[Task],
        on_success: Callable = basic_callback,
        on_failure: Callable = basic_callback,
        mode: TypeExecution = TypeExecution.SEQUENTIAL,
        keep_going: bool = False,
        workflow_id: UUID = None,
    ) -> None:
        self.tasks = tasks
        self.on_success = on_success
        self.on_failure = on_failure
        self.workflow_id = workflow_id or uuid4()
        self.started = datetime.now()

        execution = None
        groups = grouper(tasks=tasks)

        try:
            execution = getattr(self, mode)
        except AttributeError as err:
            raise ExecutionModeNotExist() from err

        self.tasks = execution(
            tasks=tasks, workflow_id=workflow_id, ignore=keep_going, groups=groups
        )

        self._callback_workflow(tasks=self.tasks)

    def _callback_workflow(self, tasks: List[Task]):
        final_status = [task.status for task in tasks]

        if TypeStatus.FAILED in final_status:
            self.on_failure(tasks=tasks)
        else:
            self.on_success(tasks=tasks)

    def sequential(self, **kwargs) -> List[Task]:
        if len(kwargs.get("groups", {})) > 1 and not is_darwin():
            process = SequentialGroup(**kwargs)
            return process.get_tasks()

        process = Sequential(**kwargs)
        return process.get_tasks()

    def sequential_group(self, **kwargs):
        process = SequentialGroup(**kwargs)
        return process.get_tasks()

    def background(self, **kwargs) -> List[Task]:
        process = Background(**kwargs)
        return process.get_tasks()

    def parallel(self, **kwargs) -> List[Task]:
        if is_darwin():
            warnings.warn(
                "Parallel mode does not work with MacOS."
                " Running tasks in sequence.",
                Warning
            )
            process = Sequential(**kwargs)
            return process.get_tasks()

        process = Parallel(**kwargs)
        return process.get_tasks()


class Sequential(Flow):
    """Sequential"""

    def setup_queue(self) -> None:
        self.queue = []

    def get_tasks(self) -> List[Task]:
        return self.queue

    def _flow_callback(self, task: Task) -> None:
        self.queue.append(task)

    def run(self) -> None:
        previous_context = Context(workflow_id=self.workflow_id)

        for task in self.tasks:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                _flow_callback=self._flow_callback,
            )

            previous_context = task.config.storage.get(
                key=task.config.storage.key(task=task)
            )

            if not self.ignore and task.status == TypeStatus.FAILED:
                break


class SequentialGroup(Flow):
    """SequentialGroup"""

    def setup_queue(self) -> None:
        self.queue = Queue()

    def get_tasks(self) -> List[Task]:
        contexts = {}
        while len(contexts) < len(self.tasks):
            if not self.queue.empty():
                contexts = {**contexts, **self.queue.get()}

        if contexts:
            for task in self.tasks:
                task.current_context = contexts[task.task_id]["current_context"]
                task.duration = contexts[task.task_id]["duration"]
                task.error = contexts[task.task_id]["error"]
                task.status = contexts[task.task_id]["status"]

        return self.tasks

    def _flow_callback(self, task: Task) -> None:
        current_task = {
            task.task_id: {
                "current_context": task.current_context,
                "duration": task.duration,
                "error": task.error,
                "status": task.status,
            }
        }
        self.queue.put(current_task)

    def run(self) -> None:
        threads = []
        processes = []

        for _, group_tasks in self.groups.items():
            thread = threading.Thread(
                target=self._launch_group,
                args=(processes, group_tasks,)
            )
            thread.start()
            threads.append(thread)

        for process in processes:
            process.join()

        for thread in threads:
            thread.join()

    def _launch_group(self, processes, group_tasks):
        process = Process(
            target=self._run_group,
            args=(group_tasks,)
        )
        process.start()
        processes.append(process)

    def _run_group(self, groups: List[Task]) -> None:
        previous_context = Context(workflow_id=self.workflow_id)

        for task in groups:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                _flow_callback=self._flow_callback,
            )

            previous_context = task.config.storage.get(
                key=task.config.storage.key(task=task)
            )

            if not self.ignore and task.status == TypeStatus.FAILED:
                break


class Background(Flow):
    """Background"""

    def setup_queue(self) -> None:
        self.queue = []

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def _flow_callback(self, task: Task) -> None:
        pass

    def run(self) -> None:
        thread = threading.Thread(
            target=Sequential,
            args=(
                self.tasks,
                self.workflow_id,
                self.ignore,
                self.groups,
            ),
        )
        thread.start()
        thread.join()


class Parallel(Flow):
    """Parallel"""

    def setup_queue(self) -> None:
        self.queue = Queue()

    def get_tasks(self) -> List[Task]:
        contexts = {}
        while len(contexts) < len(self.tasks):
            if not self.queue.empty():
                contexts = {**contexts, **self.queue.get()}

        for task in self.tasks:
            task.current_context = contexts[task.task_id]["current_context"]
            task.duration = contexts[task.task_id]["duration"]
            task.error = contexts[task.task_id]["error"]
            task.status = contexts[task.task_id]["status"]

        return self.tasks

    def _flow_callback(self, task: Task) -> None:
        current_task = {
            task.task_id: {
                "current_context": task.current_context,
                "duration": task.duration,
                "error": task.error,
                "status": task.status,
            }
        }
        self.queue.put(current_task)

    def run(self) -> None:
        processes = []
        previous_context = Context(workflow_id=self.workflow_id)

        for task in self.tasks:
            process = Process(
                target=Execution,
                args=(task, self.workflow_id, previous_context, self._flow_callback),
            )
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
