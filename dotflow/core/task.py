"""Task module"""

import json

from uuid import UUID
from typing import Any, Callable, List

from dotflow.core.config import Config
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.module import Module
from dotflow.core.serializers.task import SerializerTask
from dotflow.core.serializers.workflow import SerializerWorkflow
from dotflow.core.exception import MissingActionDecorator, NotCallableObject
from dotflow.core.types.status import TypeStatus
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
        self.group_name = None


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

        group_name (str): Group name of tasks.
    """

    def __init__(
        self,
        task_id: int,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        workflow_id: UUID = None,
        config: Config = None,
        group_name: str = "default"
    ) -> None:
        super().__init__(
            task_id,
            step,
            callback,
            initial_context,
            workflow_id,
            config,
            group_name
        )
        self.config = config
        self.group_name = group_name
        self.task_id = task_id
        self.workflow_id = workflow_id
        self.step = step
        self.callback = callback
        self.initial_context = initial_context
        self.status = TypeStatus.NOT_STARTED

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
        if isinstance(value, TaskError):
            self._error = value

        if isinstance(value, Exception):
            task_error = TaskError(value)
            self._error = task_error

            self.config.log.error(task=self)

    @property
    def status(self):
        if not self._status:
            return TypeStatus.NOT_STARTED
        return self._status

    @status.setter
    def status(self, value: TypeStatus) -> None:
        self._status = value

        self.config.notify.send(task=self)
        self.config.log.info(task=self)

    @property
    def config(self):
        if not self._config:
            return Config()
        return self._config

    @config.setter
    def config(self, value: Config):
        self._config = value

    def schema(self, max: int = None) -> SerializerTask:
        return SerializerTask(**self.__dict__, max=max)

    def result(self, max: int = None) -> SerializerWorkflow:
        item = self.schema(max=max).model_dump_json()
        return json.loads(item)


class TaskError:

    def __init__(self, error: Exception = None) -> None:
        self.exception = error
        self.traceback = traceback_error(error=error) if error else ""
        self.message = message_error(error=error) if error else ""


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
        self.queue: List[Callable] = []
        self.workflow_id = workflow_id
        self.config = config

    def add(
        self,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        group_name: str = "default"
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

            group_name (str): Group name of tasks.
        """
        if isinstance(step, list):
            for inside_step in step:
                self.add(
                    step=inside_step,
                    callback=callback,
                    initial_context=initial_context,
                    group_name=group_name
                )
            return self

        self.queue.append(
            Task(
                task_id=len(self.queue),
                step=step,
                callback=Module(value=callback),
                initial_context=initial_context,
                workflow_id=self.workflow_id,
                config=self.config,
                group_name=group_name
            )
        )

        return self

    def count(self) -> int:
        return len(self.queue)

    def clear(self) -> None:
        self.queue.clear()

    def reverse(self) -> None:
        self.queue.reverse()

    def schema(self) -> SerializerWorkflow:
        return SerializerWorkflow(
            workflow_id=self.workflow_id,
            tasks=[item.schema() for item in self.queue]
        )

    def result(self) -> SerializerWorkflow:
        item = self.schema().model_dump_json()
        return json.loads(item)
