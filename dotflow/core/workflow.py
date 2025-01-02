"""Workflow"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any

from dotflow.core.error import IncorrectTypeContext


class Context:

    def __init__(self, storage: Any = None) -> None:
        self.datetime = datetime.now()
        self.storage = storage


class Task(ABC):

    RETRY: int = 0
    CONTINUE: bool = False

    def __init__(self, task_id: int, initial_context: Context):
        self.task_id = task_id
        self.initial_context = initial_context

    @abstractmethod
    def run(self, previous_context: Context) -> Context:
        raise NotImplementedError


class WorkflowBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(self, step: Task, initial_context: Context = Context()):
        task_id = len(self.queu)
        self.queu.append(
            step(
                task_id=task_id,
                initial_context=initial_context
            )
        )
        return self


class Workflow(ABC):

    def __init__(self, initial_context: Context = Context()) -> None:
        if not isinstance(initial_context, Context):
            initial_context = Context(storage=initial_context)

        self.builder = WorkflowBuilder()
        self.initial_context = initial_context

    @abstractmethod
    def build(self) -> None:
        raise NotImplementedError
