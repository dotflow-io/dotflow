from typing import Callable, List

from dotflow.core.context import Context


def callback(*args, **kwargs):
    pass


class Task:

    def __init__(self,
                 task_id: int,
                 initial_context: Context,
                 step: Callable,
                 callback: Callable):
        self.task_id = task_id
        self.initial_context = initial_context
        self.step = step
        self.callback = callback


class TaskBuilder:

    def __init__(self) -> None:
        self.queu: List[Task] = []

    def add(self,
            step: Task,
            initial_context: Context = Context(),
            callback: Callable = callback):
        task_id = len(self.queu)

        if not isinstance(initial_context, Context):
            initial_context = Context(storage=initial_context)

        self.queu.append(
            Task(
                task_id=task_id,
                initial_context=initial_context,
                step=step,
                callback=callback
            )
        )
        return self

    def count(self) -> int:
        return len(self.queu)
