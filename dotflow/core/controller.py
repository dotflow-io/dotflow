"""Controller module"""

import threading
import logging

from uuid import uuid4
from typing import Callable, List

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.models import Execution, Status
from dotflow.core.task import Task
from dotflow.core.utils import simple
from dotflow.core.decorators import time


class Controller:

    def __init__(
        self,
        tasks: List[Task],
        success: Callable = simple,
        failure: Callable = simple,
        keep_going: bool = False,
        mode: Execution = Execution.SEQUENTIAL,
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

    @time
    def _excution(self, task: Task, previous_context: Context):
        task.workflow_id = self.workflow_id
        task.set_status(Status.IN_PROGRESS)
        task.set_previous_context(previous_context)

        try:
            current_context = task.step(previous_context=previous_context)
            if hasattr(current_context.storage.__init__, "__code__"):
                step_class = current_context.storage
                current_context = Context(storage=[])

                for func_name in dir(step_class):
                    additional_function = getattr(step_class, func_name)
                    if isinstance(additional_function, Action):
                        try:
                            current_context.storage.append(additional_function())
                        except TypeError:
                            current_context.storage.append(
                                additional_function(step_class)
                            )

            task.set_status(Status.COMPLETED)
            task.set_current_context(current_context)

        except Exception as err:
            task.set_status(Status.FAILED)
            task.error.append(err)
            logging.error(msg=err)

        finally:
            task.callback(content=task)

        return task

    def sequential(self, keep_going: bool = False):
        previous_context = Context()

        for task in self.tasks:
            self._excution(task=task, previous_context=previous_context)
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
