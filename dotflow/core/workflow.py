"""Workflow module"""

import threading

from uuid import uuid4
from typing import Callable, List

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.models import TypeExecution, Status
from dotflow.core.task import Task
from dotflow.core.utils import simple


class Workflow:

    def __init__(
        self,
        tasks: List[Task],
        success: Callable = simple,
        failure: Callable = simple,
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

    def _execution_with_class(self, step_class: Callable):
        context = Context(storage=[])

        for func_name in dir(step_class):
            additional_function = getattr(step_class, func_name)
            if isinstance(additional_function, Action):
                try:
                    context.storage.append(additional_function())
                except TypeError:
                    context.storage.append(additional_function(step_class))

        return context

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
