"""Task module"""

from uuid import UUID
from typing import Any, Callable, List

from dotflow.core.context import Context
from dotflow.core.types.status import Status
from dotflow.core.utils import store_context


def _callback(*args, **kwargs):
    pass


class Task:

    def __init__(self,
                 task_id: int,
                 step: Callable,
                 callback: Callable,
                 initial_context: Context = Context(),
                 current_context: Context = Context(),
                 previous_context: Context = Context(),
                 status: Status = Status.START,
                 error: List[Exception] = [],
                 duration: int = 0,
                 workflow_id: UUID = None):
        self.task_id = task_id
        self.step = step
        self.callback = callback
        self.initial_context = store_context(initial_context)
        self.current_context = store_context(current_context)
        self.previous_context = store_context(previous_context)
        self.status = status
        self.error = error
        self.duration = duration
        self.workflow_id = workflow_id


class TaskBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(self,
            step: Callable,
            callback: Callable = _callback,
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
