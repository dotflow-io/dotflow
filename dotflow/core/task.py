"""Task module"""

from uuid import UUID
from typing import Any, Callable, List

from dotflow.core.context import Context
from dotflow.core.status.workflow import WorkflowStatus
from dotflow.core.utils import callback


class Task:

    def __init__(self,
                 task_id: int,
                 step: Callable,
                 callback: Callable,
                 initial_context: Any = None,
                 current_context: Any = None,
                 previous_context: Any = None,
                 status: WorkflowStatus = WorkflowStatus.NOT_STARTED,
                 error: List[Exception] = [],
                 duration: int = 0,
                 workflow_id: UUID = None):
        self.task_id = task_id
        self.step = step
        self.callback = callback
        self.initial_context = Context(initial_context)
        self.current_context = Context(current_context)
        self.previous_context = Context(previous_context)
        self.status = status
        self.error = error
        self.duration = duration
        self.workflow_id = workflow_id


class TaskBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(self,
            step: Callable,
            callback: Callable = callback,
            initial_context: Any = None):

        self.queu.append(
            Task(
                task_id=len(self.queu),
                step=step,
                callback=callback,
                initial_context=initial_context,
            )
        )
        return self

    def count(self) -> int:
        return len(self.queu)

    def clear(self) -> None:
        self.queu.clear()
