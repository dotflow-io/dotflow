"""Workflow module"""

import sys
import threading
import warnings
import platform
import multiprocessing as mp

from queue import Empty
from datetime import datetime
from multiprocessing import Process, Queue

from uuid import UUID, uuid4
from typing import Callable, List

from dotflow.abc.flow import Flow
from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.types import ExecutionModeType, StatusTaskType
from dotflow.core.task import Task, QueueGroup
from dotflow.core.plugin import Plugin
from dotflow.utils import basic_callback

# mp.set_start_method("spawn", force=True)


def is_darwin_arm() -> bool:
    """Is Darwin"""
    return platform.system() == "Darwin" and platform.processor() == "arm"


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
        group (QueueGroup):
            A group containing objects of type Task.

        on_success (Callable):
            Success function to be executed after the completion of the entire
            workflow. It's essentially a callback for successful scenarios.

        on_failure (Callable):
            Failure function to be executed after the completion of the entire
            workflow. It's essentially a callback for error scenarios

        mode (ExecutionModeType):
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
        group: QueueGroup,
        plugins: Plugin,
        on_success: Callable = basic_callback,
        on_failure: Callable = basic_callback,
        mode: ExecutionModeType = ExecutionModeType.SEQUENTIAL,
        keep_going: bool = False,
        workflow_id: UUID = None,
    ) -> None:
        self.group = group
        self.plugins = plugins
        self.on_success = on_success
        self.on_failure = on_failure
        self.workflow_id = workflow_id or uuid4()
        self.started = datetime.now()
        execution = None

        try:
            execution = getattr(self, mode)
        except AttributeError as err:
            raise ExecutionModeNotExist() from err

        self.tasks = execution(
            workflow_id=workflow_id,
            ignore=keep_going,
            group=group,
            plugins=plugins
        )

        self._callback_workflow(queue_group=self.group)

    def _callback_workflow(self, queue_group: QueueGroup):
        tasks = queue_group.tasks()
        final_status = [task.status for task in tasks]

        if StatusTaskType.FAILED in final_status:
            self.on_failure(tasks=tasks)
        else:
            self.on_success(tasks=tasks)

    def sequential(self, **kwargs) -> List[Task]:
        """Sequential execution"""
        many_groups = 1
        group: QueueGroup = kwargs.get("group")

        if group.size() < many_groups:
            process = SequentialGroup(**kwargs)
            return process.transport()

        process = Sequential(**kwargs)
        return process.transport()

    def sequential_group(self, **kwargs):
        """Sequential Group execution"""
        process = SequentialGroup(**kwargs)
        return process.transport()

    def background(self, **kwargs) -> List[Task]:
        """Background execution"""
        process = Background(**kwargs)
        return process.transport()

    def parallel(self, **kwargs) -> List[Task]:
        """Parallel execution"""
        if is_darwin_arm():
            warnings.warn(
                "Parallel mode does not work with MacOS."
                " Running tasks in sequence.",
                Warning
            )
            process = Sequential(**kwargs)
            return process.transport()

        process = Parallel(**kwargs)
        return process.transport()


class Sequential(Flow):
    """Sequential"""

    def setup_queue(self) -> None:
        self.queue = []

    def transport(self) -> List[Task]:
        return self.group.tasks()

    def _flow_callback(self, task: Task) -> None:
        self.queue.append(task)

    def run(self) -> None:
        previous_context = Context(
            workflow_id=self.workflow_id
        )

        for task in self.group.tasks():
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                _flow_callback=self._flow_callback,
            )

            previous_context = task.plugins.storage.get(
                key=task.plugins.storage.key(task=task)
            )

            if not self.ignore and task.status == StatusTaskType.FAILED:
                break


class SequentialGroup(Flow):
    """Sequential Group"""

    def setup_queue(self) -> None:
        self.queue = None

        if sys.version_info >= (3, 12):
            self.queue = mp.Queue()
        else:
            self.queue = Queue()

    def transport(self) -> List[Task]:
        contexts = {}
        while len(contexts) < self.group.size():
            try:
                data = self.queue.get(timeout=1)
                contexts.update(data)
            except Empty:
                pass

        if contexts:
            for task in self.group.tasks():
                task.current_context = contexts[task.task_id]["current_context"]
                task.duration = contexts[task.task_id]["duration"]
                task.error = contexts[task.task_id]["error"]
                task.status = contexts[task.task_id]["status"]

        return self.group.tasks()

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

        for _, queue in self.group.queue.items():
            thread = threading.Thread(
                target=self._launch_group,
                args=(processes, queue,)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        for process in processes:
            process.join()

    def _launch_group(self, processes, queue):
        new_process = None

        if sys.version_info >= (3, 12):
            new_process = mp.Process
        else:
            new_process = Process

        process = new_process(
            target=self._run_group,
            args=(queue,)
        )
        process.start()
        processes.append(process)

    def _run_group(self, queue: List[Task]) -> None:
        previous_context = Context(workflow_id=self.workflow_id)

        for task in queue.tasks:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context,
                _flow_callback=self._flow_callback,
            )

            previous_context = task.plugins.storage.get(
                key=task.plugins.storage.key(task=task)
            )

            if not self.ignore and task.status == StatusTaskType.FAILED:
                break


class Background(Flow):
    """Background"""

    def setup_queue(self) -> None:
        self.queue = []

    def transport(self) -> List[Task]:
        return self.group.tasks()

    def _flow_callback(self, task: Task) -> None:
        pass

    def run(self) -> None:
        thread = threading.Thread(
            target=Sequential,
            args=(
                self.workflow_id,
                self.ignore,
                self.group,
                self.plugins
            ),
        )
        thread.start()
        thread.join()


class Parallel(Flow):
    """Parallel"""

    def setup_queue(self) -> None:
        self.queue = None

        if sys.version_info >= (3, 12):
            self.queue = mp.Queue()
        else:
            self.queue = Queue()

    def transport(self) -> List[Task]:
        contexts = {}
        while len(contexts) < self.group.size():
            if not self.queue.empty():
                contexts = {**contexts, **self.queue.get()}

        if contexts:
            for task in self.group.tasks():
                task.current_context = contexts[task.task_id]["current_context"]
                task.duration = contexts[task.task_id]["duration"]
                task.error = contexts[task.task_id]["error"]
                task.status = contexts[task.task_id]["status"]

        return self.group.tasks()

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
        new_process = None

        if sys.version_info >= (3, 12):
            new_process = mp.Process
        else:
            new_process = Process

        processes = []
        previous_context = Context(
            workflow_id=self.workflow_id
        )

        for task in self.group.tasks():
            process = new_process(
                target=Execution,
                args=(
                    task,
                    self.workflow_id,
                    previous_context,
                    self._flow_callback
                ),
            )
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
