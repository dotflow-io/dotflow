"""Task module"""

from uuid import UUID
from types import FunctionType
from typing import Any, Callable, List

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.exception import MissingStepDecorator
from dotflow.core.models.status import Status
from dotflow.core.utils import callback


class Task:

    def __init__(self,
                 task_id: int,
                 step: Callable,
                 callback: Callable,
                 initial_context: Any = None,
                 current_context: Any = None,
                 previous_context: Any = None,
                 status: Status = Status.NOT_STARTED,
                 error: List[Exception] = [],
                 duration: float = 0,
                 workflow_id: UUID = None) -> None:
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

    def set_status(self, value: Status) -> None:
        self.status = value

    def set_duration(self, value: float) -> None:
        self.duration = value

    def set_current_context(self, value: Context) -> None:
        self.current_context = value

    def set_previous_context(self, value: Context) -> None:
        self.previous_context = value


class TaskBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(self,
            step: Callable,
            callback: Callable = callback,
            initial_context: Any = None) -> None:

        is_ok = []
        if isinstance(step, Action):
            is_ok.append(True)

        if isinstance(step, FunctionType):
            if step.__name__ == "action":
                is_ok.append(True)

        if not is_ok:
            raise MissingStepDecorator()

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
