"""Controller module"""

import threading

from uuid import uuid4
from typing import Callable, List

from dotflow.core.context import Context
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.models import Execution, Status
from dotflow.core.task import Task
from dotflow.core.utils import exec
from dotflow.core.decorators import time


class Controller:

    def __init__(self,
                 tasks: List[Task],
                 success: Callable = exec,
                 failure: Callable = exec,
                 keep_going: bool = False,
                 mode: Execution = Execution.SEQUENTIAL):
        self.workflow_id = uuid4()
        self.tasks = tasks
        self.success = success
        self.failure = failure

        try:
            getattr(self, mode)(keep_going=keep_going)
        except AttributeError:
            raise ExecutionModeNotExist()

    def _callback_workflow(self, result: Task):
        final_status = [flow.status for flow in result]
        if Status.FAILED in final_status:
            self.failure(content=result)
        else:
            self.success(content=result)

    @time
    def _excution(self, task: Task, previous_context: Context):
        task.workflow_id = self.workflow_id
        task.set_status(Status.IN_PROGRESS)
        task.set_previous_context(previous_context)

        try:
            current_context = task.step(previous_context=previous_context)
            task.set_status(Status.COMPLETED)
            task.set_current_context(current_context)

        except Exception as error:
            task.set_status(Status.FAILED)
            task.error.append(error)

        task.callback(content=task)
        return task

    def sequential(self, keep_going: bool = False):
        previous_context = Context()

        for task in self.tasks:
            self._excution(
                task=task,
                previous_context=previous_context
            )
            previous_context = task.current_context

            if not keep_going:
                if task.status == Status.FAILED:
                    break

        self._callback_workflow(result=self.tasks)
        return self.tasks

    def background(self, keep_going: bool = False):
        th = threading.Thread(target=self.sequential, args=[keep_going])
        th.start()

    def parallel(self, keep_going: bool = False):
        ...

    def data_store(self, keep_going: bool = False):
        ...
