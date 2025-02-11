"""DotFlow"""

import threading

from datetime import datetime
from uuid import uuid4
from typing import Callable

from dotflow.abc.context import ABCContext
from dotflow.abc.workflow import ABCWorkflow
from dotflow.core.context import Context
from dotflow.core.task import Task


def execution_default(*args, **kwargs):
    pass


class Status:

    FAILED = "Failed"
    COMPLETED = "Completed"


class Response:

    def __init__(
        self,
        id: str,
        task: Task,
        status: str,
        previous_context: ABCContext,
        current_context: ABCContext = Context(),
        error: Exception = None,
        duration: int = 0) -> None:
        self.id = id
        self.task = task
        self.status = status
        self.previous_context = previous_context
        self.current_context = current_context
        self.error = error
        self.duration = duration


class Controller:

    def __init__(self,
                 workflow: ABCWorkflow,
                 success: Callable = execution_default,
                 failure: Callable = execution_default,
                 keep_going: bool = False,
                 mode: str = "sequential"):
        self.id = uuid4().hex
        self.workflow = workflow
        self.success = success
        self.failure = failure

        try:
            getattr(self, mode)(keep_going=keep_going)
        except AttributeError:
            raise Exception("Execution mode does not exist.")

    def _callback_workflow(self, result: Response):
        final_status = [flow.status for flow in result]
        if Status.FAILED in final_status:
            self.failure(content=result)
        else:
            self.success(content=result)

    def _excution(self, task: Task, previous_context: ABCContext):
        start_time = datetime.now()
        try:
            current_context = task.step(previous_context=previous_context)
            duration = int((datetime.now() - start_time).total_seconds())
            content = Response(
                id=self.id,
                task=task,
                status=Status.COMPLETED,
                previous_context=previous_context,
                current_context=current_context,
                error=None,
                duration=duration
            )
        except Exception as error:
            duration = int((datetime.now() - start_time).total_seconds())
            content = Response(
                id=self.id,
                task=task,
                status=Status.FAILED,
                previous_context=previous_context,
                current_context=Context(),
                error=error,
                duration=duration
            )

        task.callback(content=content)
        return content

    def sequential(self, keep_going: bool = False):
        result = []
        previous_context = Context()

        for task in self.workflow.task.queu:
            content = self._excution(
                task=task,
                previous_context=previous_context
            )
            previous_context = content.current_context
            result.append(content)

            if not keep_going:
                if content.status == Status.FAILED:
                    break

        self._callback_workflow(result=result)
        return result

    def background(self, keep_going: bool = False):
        th = threading.Thread(target=self.sequential, args=[keep_going])
        th.start()

    def parallel(self):
        ...

    def data_store(self):
        ...
