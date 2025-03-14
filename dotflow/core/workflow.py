"""Workflow module"""

import threading
from datetime import datetime

from uuid import UUID, uuid4
from typing import Callable, List

from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.types import TypeExecution, TaskStatus
from dotflow.core.task import Task
from dotflow.utils import basic_callback


class Workflow:
    """
    Import:
        You can import the **Workflow** class with:

            from dotflow.core.workflow import Workflow

    Example:
        `class` dotflow.core.workflow.Workflow

            workflow = Workflow(
                tasks=[tasks],
                success=basic_callback,
                failure=basic_callback,
                keep_going=True
            )

    Args:
        tasks (List[Task]):

        success (Callable):

        failure (Callable):

        keep_going (bool):
            A parameter that receives a boolean object with the purpose of continuing
            or not the execution of the workflow in case of an error during the
            execution of a task. If it is **true**, the execution will continue;
            if it is **False**, the workflow will stop.

        mode (TypeExecution):
            A parameter for assigning the execution mode of the workflow. Currently,
            there is the option to execute in **sequential** mode or **background** mode.
            By default, it is in **sequential** mode.

        id (UUID):

    Attributes:
        id (UUID)
        started (datetime):
        tasks (List[Task]):
        success (Callable):
        failure (Callable):
    """

    def __init__(
        self,
        tasks: List[Task],
        success: Callable = basic_callback,
        failure: Callable = basic_callback,
        keep_going: bool = False,
        mode: TypeExecution = TypeExecution.SEQUENTIAL,
        id: UUID = uuid4()
    ) -> None:
        self.id = id
        self.started = datetime.now()
        self.tasks = tasks
        self.success = success
        self.failure = failure

        try:
            getattr(self, mode)(keep_going=keep_going)
        except AttributeError as err:
            raise ExecutionModeNotExist() from err

    def _callback_workflow(self, tasks: Task):
        final_status = [task.status for task in tasks]
        if TaskStatus.FAILED in final_status:
            self.failure(tasks=tasks)
        else:
            self.success(tasks=tasks)

    def sequential(self, keep_going: bool = False):
        previous_context = Context(
            workflow_id=self.id
        )

        for task in self.tasks:
            Execution(
                task=task,
                workflow_id=self.id,
                previous_context=previous_context
            )
            previous_context = task.current_context

            if not keep_going:
                if task.status == TaskStatus.FAILED:
                    break

        self._callback_workflow(tasks=self.tasks)
        return self.tasks

    def background(self, keep_going: bool = False):
        th = threading.Thread(target=self.sequential, args=[keep_going])
        th.start()

    def parallel(self, keep_going: bool = False):
        """Not implemented"""

    def data_store(self, keep_going: bool = False):
        """Not implemented"""
