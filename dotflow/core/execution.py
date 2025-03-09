"""Execution module"""

from uuid import UUID
from typing import Callable

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.types import TaskStatus

from dotflow.core.decorators import time


class Execution:

    def __init__(
        self,
        task: Task,
        workflow_id: UUID,
        previous_context: Context
    ) -> None:
        self.task = task
        self.task.status = TaskStatus.IN_PROGRESS
        self.task.previous_context = previous_context
        self.task.workflow_id = workflow_id

        self._excution()

    def _is_action(self, class_instance: Callable, func: Callable):
        return (
            callable(getattr(class_instance, func))
            and not func.startswith("__")
            and getattr(class_instance, func).__module__ is Action.__module__
        )

    def _execution_with_class(self, class_instance: Callable):
        new_context = Context(storage=[])
        previous_context = self.task.previous_context
        callable_list = [func for func in dir(class_instance) if self._is_action(class_instance, func)]

        for callable_name in callable_list:
            new_object = getattr(class_instance, callable_name)
            try:
                subcontext = new_object(
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                )
                new_context.storage.append(subcontext)
                previous_context = subcontext

            except TypeError:
                subcontext = new_object(
                    class_instance,
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                )
                new_context.storage.append(subcontext)
                previous_context = subcontext

        if not new_context.storage:
            return Context(storage=class_instance)

        return new_context

    @time
    def _excution(self):
        try:
            current_context = self.task.step(
                initial_context=self.task.initial_context,
                previous_context=self.task.previous_context,
            )

            if type(current_context.storage) not in [str, int, float, dict, list]:
                current_context = self._execution_with_class(
                    class_instance=current_context.storage
                )

            self.task.status = TaskStatus.COMPLETED
            self.task.current_context = current_context

        except Exception as err:
            self.task.status = TaskStatus.FAILED
            self.task.error = err

        finally:
            self.task.callback(content=self.task)

        return self.task
