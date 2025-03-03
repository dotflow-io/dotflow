"""Workflow module"""

import threading

from uuid import uuid4
from typing import Callable, List

from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.models import TypeExecution, Status
from dotflow.core.task import Task
from dotflow.core.utils import basic_callback


class Workflow:

    def __init__(
        self,
        tasks: List[Task],
        success: Callable = basic_callback,
        failure: Callable = basic_callback,
        keep_going: bool = False,
        mode: TypeExecution = TypeExecution.SEQUENTIAL,
    ) -> None:
        self.workflow_id = uuid4()
        self.tasks = tasks
        self.success = success
        self.failure = failure

        try:
            getattr(self, mode)(keep_going=keep_going)
        except AttributeError as err:
            raise ExecutionModeNotExist() from err

    def _callback_workflow(self, tasks: Task):
        final_status = [task.status for task in tasks]
        if Status.FAILED in final_status:
            self.failure(tasks=tasks)
        else:
            self.success(tasks=tasks)

    def sequential(self, keep_going: bool = False):
        previous_context = Context()

        for task in self.tasks:
            Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=previous_context
            )
            previous_context = task.current_context

            if not keep_going:
                if task.status == Status.FAILED:
                    break

        self._callback_workflow(tasks=self.tasks)
        return self.tasks

    def background(self, keep_going: bool = False):
        th = threading.Thread(target=self.sequential, args=[keep_going])
        th.start()

    def parallel(self, keep_going: bool = False): ...

    def data_store(self, keep_going: bool = False): ...
