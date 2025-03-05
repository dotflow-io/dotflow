"""Execution module"""

from uuid import UUID
from typing import Callable

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.models import TaskStatus

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
        self.task._set_workflow_id(workflow_id)
        self.task.previous_context = previous_context

        self._excution()

    def _execution_with_class(self, class_instance: Callable):
        context = Context(storage=[])
        previous_context = self.task.previous_context

        for func_name in dir(class_instance):
            additional_function = getattr(class_instance, func_name)

            if isinstance(additional_function, Action):
                try:
                    current_context = additional_function(
                        initial_context=self.task.initial_context,
                        previous_context=previous_context,
                    )
                    context.storage.append(current_context)
                    previous_context = current_context
                except TypeError:
                    current_context = additional_function(
                        class_instance,
                        initial_context=self.task.initial_context,
                        previous_context=previous_context,
                    )
                    context.storage.append(current_context)
                    previous_context = current_context

        if not context.storage:
            return Context(storage=class_instance)

        return context

    @time
    def _excution(self):
        try:
            current_context = self.task.step(
                initial_context=self.task.initial_context,
                previous_context=self.task.previous_context,
            )

            object_attributes = [
                type(getattr(current_context.storage, param)) is Action
                for param in dir(current_context.storage)
            ]

            if True in object_attributes:
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
