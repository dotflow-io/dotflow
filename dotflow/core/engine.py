"""TaskEngine module"""

import re
from collections.abc import Callable
from contextlib import contextmanager
from datetime import datetime
from inspect import getsourcelines
from types import FunctionType
from uuid import UUID

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.exception import ExecutionWithClassError
from dotflow.core.task import Task
from dotflow.core.types import TypeStatus
from dotflow.logging import logger


class TaskEngine:
    """Manages the execution lifecycle of a single task.

    Separates the task lifecycle (status, duration, error handling)
    from how tasks are executed (sequential, parallel, background).
    """

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
    ) -> None:
        self.task = task
        self.workflow_id = workflow_id
        self.previous_context = previous_context
        self._start_time = None

    @contextmanager
    def start(self):
        """Prepares the task for execution and manages its lifecycle."""
        self.task.workflow_id = self.workflow_id
        self.task.previous_context = self.previous_context
        self.task.config.tracer.start_task(task=self.task)
        self.task.status = TypeStatus.IN_PROGRESS
        self._start_time = datetime.now()

        try:
            yield self
        except AssertionError as err:
            raise err
        except Exception as err:
            self.task.errors = err
            self.task.current_context = None
            self.task.status = TypeStatus.FAILED
        else:
            self.task.duration = (
                datetime.now() - self._start_time
            ).total_seconds()
            if self.task.status in (
                TypeStatus.IN_PROGRESS,
                TypeStatus.RETRY,
            ):
                self.task.status = TypeStatus.COMPLETED
        finally:
            self.task.config.tracer.end_task(task=self.task)

    @contextmanager
    def timeout_context(self, seconds: int):
        """Wraps execution block with a timeout.

        If seconds is 0 or None, no timeout is applied.

        Args:
            seconds: Maximum execution time in seconds.
        """
        if not seconds:
            yield
            return

        start = datetime.now()
        yield
        elapsed = (datetime.now() - start).total_seconds()
        if elapsed > seconds:
            raise TimeoutError(
                f"Task exceeded timeout of {seconds}s (took {elapsed:.2f}s)"
            )

    @contextmanager
    def checkpoint_context(self):
        """Saves a checkpoint after successful execution."""
        yield
        if self.task.status != TypeStatus.FAILED:
            self.task.config.storage.post(
                key=self.task.config.storage.key(task=self.task),
                context=self.task.current_context,
            )

    def execute(self):
        """Executes the task function and returns the context."""
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
        return current_context

    def _is_action(self, class_instance: Callable, func: Callable):
        try:
            return (
                callable(getattr(class_instance, func))
                and getattr(class_instance, func).__module__
                == Action.__module__
                and not func.startswith("__")
            )
        except AttributeError:
            return False

    def _execution_orderer(
        self, callable_list: list[str], class_instance: Callable
    ) -> tuple[int, Callable]:
        ordered_list = []

        try:
            inside_code = getsourcelines(class_instance.__class__)[0]

            for callable_name in callable_list:
                pattern = re.compile(
                    rf"\bdef\s+{re.escape(callable_name)}\s*\("
                )
                for index, code in enumerate(inside_code):
                    if pattern.search(code):
                        ordered_list.append((index, callable_name))
                        break

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
