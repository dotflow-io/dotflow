"""Execution module"""

from uuid import UUID
from typing import Callable, List, Tuple
from inspect import getsourcelines
from types import FunctionType

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from dotflow.logging import logger
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.types import TaskStatus
from dotflow.core.decorators import time


class Execution:

    VALID_OBJECTS = [
        str,
        int,
        float,
        complex,
        dict,
        list,
        tuple,
        set,
        frozenset,
        range,
        bool,
        FunctionType,
        NoneType,
        bytes,
        bytearray,
        memoryview,
    ]

    def __init__(
        self,
        task: Task,
        workflow_id: UUID,
        previous_context: Context = None
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

    def _execution_orderer(
            self,
            callable_list: List[str],
            class_instance: Callable
    ) -> Tuple[int, Callable]:
        ordered_list = []

        try:
            inside_code = getsourcelines(class_instance.__class__)[0]

            for callable_name in callable_list:
                for index, code in enumerate(inside_code):
                    if code.find(f"def {callable_name}") != -1:
                        ordered_list.append((index, callable_name))

            ordered_list.sort()
            return ordered_list

        except TypeError as err:
            logger.error("Internal problem: %s", str(err))

        for index, callable_name in enumerate(callable_list):
            ordered_list.append((index, callable_name))

        return ordered_list

    def _execution_with_class(self, class_instance: Callable):
        new_context = Context(storage=[])
        previous_context = self.task.previous_context
        callable_list = [
            func
            for func in dir(class_instance)
            if self._is_action(class_instance, func)
        ]

        ordered_list = self._execution_orderer(
            callable_list=callable_list, class_instance=class_instance
        )

        for _, new in ordered_list:
            new_object = getattr(class_instance, new)
            try:
                subcontext = new_object(
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                    task=self.task
                )
                new_context.storage.append(subcontext)
                previous_context = subcontext

            except Exception:
                subcontext = new_object(
                    class_instance,
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                    task=self.task
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
                task=self.task
            )

            if type(current_context.storage) not in self.VALID_OBJECTS:
                current_context = self._execution_with_class(
                    class_instance=current_context.storage
                )

            self.task.status = TaskStatus.COMPLETED
            self.task.current_context = current_context

        except AssertionError as err:
            raise err

        except Exception as err:
            self.task.status = TaskStatus.FAILED
            self.task.current_context = None
            self.task.error = err

        finally:
            self.task.callback(content=self.task)

        return self.task
