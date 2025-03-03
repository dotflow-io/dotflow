"""Task module"""

from uuid import UUID
from typing import Any, Callable, List

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.module import Module
from dotflow.core.exception import MissingActionDecorator
from dotflow.core.models.status import Status
from dotflow.core.utils import (
    basic_callback,
    traceback_error,
    message_error
)


class Task:

    def __init__(
        self,
        task_id: int,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
    ) -> None:
        self.task_id = task_id
        self.step = step
        self.callback = callback
        self.initial_context = Context(initial_context)
        self.current_context = Context()
        self.previous_context = Context()
        self.status = Status.NOT_STARTED
        self.error = TaskError()
        self.duration = 0
        self.workflow_id = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        self._status = value

    def _set_status(self, value: Status) -> None:
        self.status = value

    def _set_duration(self, value: float) -> None:
        self.duration = value

    def _set_current_context(self, value: Context) -> None:
        self.current_context = value

    def _set_previous_context(self, value: Context) -> None:
        self.previous_context = value

    def _set_workflow_id(self, value: UUID) -> None:
        self.workflow_id = value

    def _set_error(self, value: Exception) -> None:
        self.error._set(error=value)


class TaskError:

    def __init__(self):
        self.exception = None
        self.traceback = None
        self.message = None

    def _set(self, error: Exception):
        self.exception = error
        self.traceback = traceback_error(error=error)
        self.message = message_error(error=error)


class TaskBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(
        self,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None
    ) -> None:
        step = Module(value=step)

        if step.__module__ != Action.__module__:
            raise MissingActionDecorator()

        self.queu.append(
            Task(
                task_id=len(self.queu),
                step=step,
                callback=Module(value=callback),
                initial_context=initial_context,
            )
        )

        return self

    def count(self) -> int:
        return len(self.queu)

    def clear(self) -> None:
        self.queu.clear()
