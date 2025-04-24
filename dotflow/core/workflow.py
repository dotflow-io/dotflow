"""Workflow module"""

import threading

from datetime import datetime
from multiprocessing import Process, Queue

from uuid import UUID, uuid4
from typing import Callable, Dict, List

from dotflow.abc.flow import Flow
from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.types import TypeExecution, TaskStatus
from dotflow.core.task import Task
from dotflow.utils import basic_callback


def grouper(tasks: List[Task]) -> Dict[str, List[Task]]:
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
                success=basic_callback,
                failure=basic_callback,
                keep_going=True
            )

    Args:
        tasks (List[Task]):
            A list containing objects of type Task.

        success (Callable):
            Success function to be executed after the completion of the entire
            workflow. It's essentially a callback for successful scenarios.

        failure (Callable):
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

        workflow_id (UUID):

    Attributes:
        success (Callable):
        failure (Callable):
        workflow_id (UUID):
        started (datetime):
    """

    def __init__(
        self,
        tasks: List[Task],
        success: Callable = basic_callback,
        failure: Callable = basic_callback,
        mode: TypeExecution = TypeExecution.SEQUENTIAL,
        keep_going: bool = False,
        workflow_id: UUID = None
    ) -> None:
        self.tasks = tasks
        self.success = success
        self.failure = failure
        self.workflow_id = workflow_id or uuid4()
        self.started = datetime.now()

        execution = None
        groups = grouper(tasks=tasks)

        try:
            execution = getattr(self, mode)
        except AttributeError as err:
            raise ExecutionModeNotExist() from err

        self.tasks = execution(
            tasks=tasks,
            workflow_id=workflow_id,
            ignore=keep_going,
            groups=groups
        )

        self._callback_workflow(tasks=self.tasks)

    def _callback_workflow(self, tasks: List[Task]):
        final_status = [task.status for task in tasks]

        if TaskStatus.FAILED in final_status:
            self.failure(tasks=tasks)
        else:
            self.success(tasks=tasks)

    def sequential(self, **kwargs) -> List[Task]:
        if len(kwargs.get("groups")) > 1:
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
        process = Parallel(**kwargs)
        return process.get_tasks()


class Sequential(Flow):

    def setup_queue(self) -> None:
        self.queue = []

    def get_tasks(self) -> List[Task]:
        return self.queue

    def internal_callback(self, task: Task) -> None:
        self.queue.append(task)

    def run(self) -> None:
        previous_context = Context(
            workflow_id=self.workflow_id
        )

        for task in self.tasks:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                internal_callback=self.internal_callback
            )

            previous_context = task.config.storage.get(
                key=task.config.storage.key(task=task)
            )

            if not self.ignore:
                if task.status == TaskStatus.FAILED:
                    break


class SequentialGroup(Flow):

    def setup_queue(self) -> None:
        self.queue = Queue()

    def get_tasks(self) -> List[Task]:
        contexts = {}
        while len(contexts) < len(self.groups):
            if not self.queue.empty():
                contexts = {**contexts, **self.queue.get()}

        if contexts:
            for task in self.tasks:
                task.current_context = contexts[task.task_id]["current_context"]
                task.duration = contexts[task.task_id]["duration"]
                task.error = contexts[task.task_id]["error"]
                task.status = contexts[task.task_id]["status"]

        return self.tasks

    def internal_callback(self, task: Task) -> None:
        current_task = {
            task.task_id: {
                "current_context": task.current_context,
                "duration": task.duration,
                "error": task.error,
                "status": task.status
            }
        }
        self.queue.put(current_task)

    def run(self) -> None:
        thread_list = []
        process_list = []

        for group in self.groups:
            def parallel(process_list):
                process = Process(
                    target=self.sequential,
                    args=(self.groups[group],)
                )
                process.start()
                process_list.append(process)

            thread = threading.Thread(
                target=parallel,
                args=(process_list,)
            )
            thread.start()
            thread_list.append(thread)

        [process.join() for process in process_list]
        [thread.join() for thread in thread_list]

    def sequential(self, groups: List[Task]) -> None:
        previous_context = Context(workflow_id=self.workflow_id)

        for task in groups:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                internal_callback=self.internal_callback
            )

            previous_context = task.config.storage.get(
                key=task.config.storage.key(task=task)
            )

            if not self.ignore:
                if task.status == TaskStatus.FAILED:
                    break


class Background(Flow):

    def setup_queue(self) -> None:
        self.queue = []

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def internal_callback(self, task: Task) -> None:
        pass

    def run(self) -> None:
        thread = threading.Thread(
            target=Sequential,
            args=(self.tasks, self.workflow_id, self.ignore,)
        )
        thread.start()
        thread.join()


class Parallel(Flow):

    def setup_queue(self) -> None:
        self.queue = Queue()

    def get_tasks(self) -> List[Task]:
        contexts = {}
        while len(contexts) < len(self.groups):
            if not self.queue.empty():
                contexts = {**contexts, **self.queue.get()}

        for task in self.tasks:
            task.current_context = contexts[task.task_id]["current_context"]
            task.duration = contexts[task.task_id]["duration"]
            task.error = contexts[task.task_id]["error"]
            task.status = contexts[task.task_id]["status"]

        return self.tasks

    def internal_callback(self, task: Task) -> None:
        current_task = {
            task.task_id: {
                "current_context": task.current_context,
                "duration": task.duration,
                "error": task.error,
                "status": task.status
            }
        }
        self.queue.put(current_task)

    def run(self) -> None:
        process_list = []
        previous_context = Context(
            workflow_id=self.workflow_id
        )

        for task in self.tasks:
            process = Process(
                target=Execution,
                args=(
                    task,
                    self.workflow_id,
                    previous_context,
                    self.internal_callback
                )
            )
            process.start()
            process_list.append(process)

        [process.join() for process in process_list]
