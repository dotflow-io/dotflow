"""Execution module"""

from uuid import UUID
from datetime import datetime
from typing import Callable, List, Tuple
from inspect import getsourcelines
from types import FunctionType

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from dotflow.core.exception import ExecutionWithClassError
from dotflow.logging import logger
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.types import TypeStatus

from dotflow.utils import basic_callback


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
        previous_context: Context = None,
        _flow_callback: Callable = basic_callback,
    ) -> None:
        self.task = task
        self.task.status = TypeStatus.IN_PROGRESS
        self.task.previous_context = previous_context
        self.task.workflow_id = workflow_id

        self._excution(_flow_callback)

    def _is_action(self, class_instance: Callable, func: Callable):
        try:
            return (
                callable(getattr(class_instance, func))
                and getattr(class_instance, func).__module__ is Action.__module__
                and not func.startswith("__")
            )
        except AttributeError:
            return False

    def _execution_orderer(
        self, callable_list: List[str], class_instance: Callable
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
            logger.error(
                "Internal problem with ordering the class functions, but don't worry, it was executed.: %s",
                str(err),
            )

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

        for index, new in enumerate(ordered_list):
            new_object = getattr(class_instance, new[1])
            try:
                subcontext = new_object(
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                    task=self.task,
                )
                subcontext.task_id = index
                new_context.storage.append(subcontext)
                previous_context = subcontext

            except Exception as error:
                if not isinstance(error, ExecutionWithClassError):
                    raise error

                subcontext = new_object(
                    class_instance,
                    initial_context=self.task.initial_context,
                    previous_context=previous_context,
                    task=self.task,
                )
                subcontext.task_id = index
                new_context.storage.append(subcontext)
                previous_context = subcontext

        if not new_context.storage:
            return Context(storage=class_instance)

        return new_context

    def _excution(self, _flow_callback):
        try:
            start = datetime.now()
            current_context = self.task.step(
                initial_context=self.task.initial_context,
                previous_context=self.task.previous_context,
                task=self.task,
            )

            if type(current_context.storage) not in self.VALID_OBJECTS:
                current_context = self._execution_with_class(
                    class_instance=current_context.storage
                )

            self.task.current_context = current_context
            self.task.duration = (datetime.now() - start).total_seconds()
            self.task.status = TypeStatus.COMPLETED

        except AssertionError as err:
            raise err

        except Exception as err:
            self.task.error = err
            self.task.current_context = None
            self.task.status = TypeStatus.FAILED

        finally:
            self.task.callback(task=self.task)
            _flow_callback(task=self.task)

        return self.task
