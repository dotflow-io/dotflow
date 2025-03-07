"""Task module"""

from uuid import UUID
from typing import Any, Callable, List

from dotflow.log import logger
from dotflow.core.config import Config
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.module import Module
from dotflow.core.exception import MissingActionDecorator, NotCallableObject
from dotflow.core.types.status import TaskStatus
from dotflow.settings import Settings as settings
from dotflow.utils import basic_callback, traceback_error, message_error, copy_file


class TaskInstance:

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

    def __init__(
        self,
        task_id: int,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        workflow_id: UUID = None,
        config: Config = None,
    ) -> None:
        super().__init__(task_id, step, callback, initial_context, workflow_id)
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

        if self.config.output:
            logger.info(
                "ID %s - %s - Initial Context -> %s",
                self.workflow_id,
                self.task_id,
                str(value),
            )

        copy_file(source=settings.LOG_PATH, destination=self.config.log_path)

    @property
    def current_context(self):
        if not self._current_context:
            return Context()
        return self._current_context

    @current_context.setter
    def current_context(self, value: Context):
        self._current_context = Context(value)

        if self.config.output:
            logger.info(
                "ID %s - %s - Current Context -> %s",
                self.workflow_id,
                self.task_id,
                str(value.storage),
            )

        copy_file(source=settings.LOG_PATH, destination=self.config.log_path)

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
            value
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

    def __init__(self, config: Config, workflow_id: UUID = None) -> None:
        self.queu: List[Callable] = []
        self.workflow_id = workflow_id
        self.config = config

    def add(
        self,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
    ) -> None:
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
