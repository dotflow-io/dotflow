"""Task module"""

from uuid import UUID
from typing import Any, Callable, List

from rich.console import Console  # type: ignore

from dotflow.logging import logger
from dotflow.core.config import Config
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.module import Module
from dotflow.core.exception import MissingActionDecorator, NotCallableObject
from dotflow.core.types.status import TaskStatus
from dotflow.utils import (
    basic_callback,
    traceback_error,
    message_error
)


class TaskInstance:
    """
    Import:
        You can import the **TaskInstance** class with:

            from dotflow.core.task import TaskInstance
    """

    def __init__(self, *args, **kwargs) -> None:
        self.task_id = None
        self.workflow_id = None
        self._step = None
        self._callback = None
        self._previous_context = None
        self._initial_context = None
        self._current_context = None
        self._duration = None
        self._error = None
        self._status = None
        self._config = None


class Task(TaskInstance):
    """
    Import:
        You can import the **Task** class directly from dotflow:

            from dotflow import Task

    Example:
        `class` dotflow.core.task.Task

            task = Task(
                task_id=1,
                step=my_step,
                callback=my_callback
            )

    Args:
        task_id (int): Task ID.

        step (Callable):
            A argument that receives an object of the callable type,
            which is basically a function. You can see in this
            [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function).

        callback (Callable):
            Any callable object that receives **args** or **kwargs**,
            which is basically a function. You can see in this
            [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#2-callback-function).

        initial_context (Any): Any python object.

        workflow_id (UUID): Workflow ID.

        config (Config): Configuration class.
    """

    def __init__(
        self,
        task_id: int,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        workflow_id: UUID = None,
        config: Config = None,
    ) -> None:
        super().__init__(
            task_id,
            step,
            callback,
            initial_context,
            workflow_id
        )
        self.task_id = task_id
        self.workflow_id = workflow_id
        self.step = step
        self.callback = callback
        self.initial_context = initial_context
        self.status = TaskStatus.NOT_STARTED
        self.config = config

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value: Callable):
        new_step = value

        if isinstance(value, str):
            new_step = Module(value=value)

        if new_step.__module__ != Action.__module__:
            raise MissingActionDecorator()

        self._step = new_step

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value: Callable):
        new_callback = value

        if isinstance(value, str):
            new_callback = Module(value=value)

        if not isinstance(new_callback, Callable):
            raise NotCallableObject(name=str(new_callback))

        self._callback = new_callback

    @property
    def previous_context(self):
        if not self._previous_context:
            return Context()
        return self._previous_context

    @previous_context.setter
    def previous_context(self, value: Context):
        self._previous_context = Context(value)

    @property
    def initial_context(self):
        if not self._initial_context:
            return Context()
        return self._initial_context

    @initial_context.setter
    def initial_context(self, value: Context):
        self._initial_context = Context(value)

    @property
    def current_context(self):
        if not self._current_context:
            return Context()
        return self._current_context

    @current_context.setter
    def current_context(self, value: Context):
        self._current_context = Context(
            task_id=self.task_id,
            workflow_id=self.workflow_id,
            storage=value
        )

        self.config.storage.post(
            key=self.config.storage.key(task=self),
            context=self.current_context
        )

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = value

    @property
    def error(self):
        if not self._error:
            return TaskError()
        return self._error

    @error.setter
    def error(self, value: Exception) -> None:
        task_error = TaskError(value)
        self._error = task_error

        logger.error(
            "ID %s - %s - %s \n %s",
            self.workflow_id,
            self.task_id,
            self.status,
            task_error.traceback,
        )

        console = Console()
        console.print_exception(show_locals=True)

    @property
    def status(self):
        if not self._status:
            return TaskStatus.NOT_STARTED
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        self._status = value

        logger.info(
            "ID %s - %s - %s",
            self.workflow_id,
            self.task_id,
            self.status,
        )

    @property
    def config(self):
        if not self._config:
            return Config()
        return self._config

    @config.setter
    def config(self, value: Config):
        self._config = value


class TaskError:

    def __init__(self, error: Exception = None) -> None:
        self.exception = error
        self.traceback = traceback_error(error=error)
        self.message = message_error(error=error)


class TaskBuilder:
    """
    Import:
        You can import the **Task** class with:

            from dotflow.core.task import TaskBuilder

    Example:
        `class` dotflow.core.task.TaskBuilder

            from uuid import uuid4

            build = TaskBuilder(
                config=config
                workflow_id=uuid4()
            )

    Args:
        config (Config): Configuration class.
        workflow_id (UUID): Workflow ID.
    """

    def __init__(
            self,
            config: Config,
            workflow_id: UUID = None
    ) -> None:
        self.queu: List[Callable] = []
        self.workflow_id = workflow_id
        self.config = config

    def add(
        self,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
    ) -> None:
        """
        Args:
            step (Callable):
                A argument that receives an object of the callable type,
                which is basically a function. You can see in this
                [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function).

            callback (Callable):
                Any callable object that receives **args** or **kwargs**,
                which is basically a function. You can see in this
                [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#2-callback-function).

            initial_context (Context):
                The argument exists to include initial data in the execution
                of the workflow within the **function context**. This parameter
                can be accessed internally, for example: **initial_context**,
                to retrieve this information and manipulate it if necessary,
                according to the objective of the workflow.
        """
        if isinstance(step, list):
            for inside_step in step:
                self.add(
                    step=inside_step,
                    callback=callback,
                    initial_context=initial_context
                )
            return self

        self.queu.append(
            Task(
                task_id=len(self.queu),
                step=step,
                callback=Module(value=callback),
                initial_context=initial_context,
                workflow_id=self.workflow_id,
                config=self.config,
            )
        )

        return self

    def count(self) -> int:
        return len(self.queu)

    def clear(self) -> None:
        self.queu.clear()

    def reverse(self) -> None:
        self.queu.reverse()
