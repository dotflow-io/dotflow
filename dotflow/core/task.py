"""Task module"""

import json

from uuid import UUID
from typing import Any, Callable, List, Dict

from dotflow.abc.logs import TypeLog
from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.module import Module
from dotflow.core.plugin import Plugin
from dotflow.core.serializers.task import SerializerTask
from dotflow.core.serializers.workflow import SerializerWorkflow
from dotflow.core.exception import MissingActionDecorator, NotCallableObject
from dotflow.core.types.status import StatusTaskType, TYPE_STATUS_TASK
from dotflow.utils import (
    basic_callback,
    traceback_error,
    message_error
)

INITIAL_INDEX = 0
TASK_GROUP_NAME = "standard"


class TaskInstance:
    """
    Import:
        You can import the **TaskInstance** class with:

            from dotflow.core.task import TaskInstance
    """

    def __init__(self, *_args, **_kwargs) -> None:
        self.task_id = None
        self._step = None
        self.plugins = None
        self._callback = None
        self._initial_context = None
        self.workflow_id = None
        self.group_name = None
        self._previous_context = None
        self._current_context = None
        self._duration = None
        self._error = None
        self._status = None


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
                plugins=plugins,
                callback=my_callback
            )

    Args:
        task_id (int): Task ID.

        step (Callable):
            A argument that receives an object of the callable type,
            which is basically a function. You can see in this
            [example](https://dotflow-io.github.io/dotflow/nav/tutorial/first-steps/#3-task-function).

        plugins (Plugin): Plugin class.

        callback (Callable):
            Any callable object that receives **args** or **kwargs**,
            which is basically a function. You can see in this
            [example](https://dotflow-io.github.io/dotflow/nav/tutorial/first-steps/#2-callback-function).

        initial_context (Any): Any python object.

        workflow_id (UUID): Workflow ID.

        group_name (str): Group name of tasks.
    """

    def __init__(
        self,
        task_id: int,
        step: Callable,
        plugins: Plugin,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        workflow_id: UUID = None,
        group_name: str = TASK_GROUP_NAME
    ) -> None:
        super().__init__(
            task_id,
            step,
            plugins,
            callback,
            initial_context,
            workflow_id,
            group_name
        )
        self.task_id = task_id
        self.step = step
        self.plugins = plugins
        self.callback = callback
        self.initial_context = initial_context
        self.workflow_id = workflow_id
        self.group_name = group_name
        self.previous_context = None
        self.current_context = None
        self.duration = None
        self.error = None
        self.status = StatusTaskType.IN_QUEUE

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

        self.plugins.storage.post(
            key=self.plugins.storage.key(task=self),
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
        if not value:
            self._error = TaskError()

        if isinstance(value, TaskError):
            self._error = value

        if isinstance(value, Exception):
            task_error = TaskError(error=value)
            self._error = task_error

    @property
    def status(self):
        if not self._status:
            return StatusTaskType.IN_QUEUE
        return self._status

    @status.setter
    def status(self, value: TYPE_STATUS_TASK) -> None:
        self._status = value

        self.plugins.notify.send(task_object=self)

        self.plugins.logs.on_task_status_change(
            task_object=self,
            type=TypeLog.INFO
        )

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
        You can import the **TaskBuilder** class with:

            from dotflow.core.task import TaskBuilder

    Example:
        `class` dotflow.core.task.TaskBuilder

            from uuid import uuid4

            build = TaskBuilder(
                plugins=plugins
                workflow_id=uuid4()
            )

    Args:
        plugins (Plugin): Plugin class.

        workflow_id (UUID): Workflow ID.

    Attributes:
        group (QueueGroup):

        workflow_id (UUID):

        plugins (Plugin)

    """

    def __init__(
            self,
            plugins: Plugin,
            workflow_id: UUID = None
    ) -> None:
        self.group: QueueGroup = QueueGroup()
        self.workflow_id = workflow_id
        self.plugins = plugins

    def add(
        self,
        step: Callable,
        callback: Callable = basic_callback,
        initial_context: Any = None,
        group_name: str = TASK_GROUP_NAME
    ) -> None:
        """
        Args:
            step (Callable):
                A argument that receives an object of the callable type,
                which is basically a function. You can see in this
                [example](https://dotflow-io.github.io/dotflow/nav/tutorial/first-steps/#3-task-function).

            callback (Callable):
                Any callable object that receives **args** or **kwargs**,
                which is basically a function. You can see in this
                [example](https://dotflow-io.github.io/dotflow/nav/tutorial/first-steps/#2-callback-function).

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

        self.group.add(
            item=Task(
                task_id=self.group.size(),
                step=step,
                callback=Module(value=callback),
                initial_context=initial_context,
                workflow_id=self.workflow_id,
                plugins=self.plugins,
                group_name=group_name
            )
        )

        return self

    def count(self, group_name: str = TASK_GROUP_NAME) -> int:
        return self.group.queue[group_name].size()

    def clear(self, group_name: str = TASK_GROUP_NAME) -> None:
        self.group.queue[group_name].clear()

    def reverse(self, group_name: str = TASK_GROUP_NAME) -> None:
        self.group.queue[group_name].reverse()

    def schema(self) -> SerializerWorkflow:
        return SerializerWorkflow(
            workflow_id=self.workflow_id,
            tasks=[item.schema() for item in self.group.tasks()]
        )

    def result(self) -> SerializerWorkflow:
        item = self.schema().model_dump_json()
        return json.loads(item)


class QueueGroup:

    def __init__(self):
        self.queue: Dict[str, Queue] = {}

    def add(self, item: Task) -> None:
        if not self.queue.get(item.group_name):
            self.queue[item.group_name] = Queue()

        self.queue[item.group_name].add(item=item)

    def size(self) -> int:
        current_size = 0
        for _, group in self.queue.items():
            current_size += group.size()

        return current_size

    def count(self) -> int:
        return len(self.queue)

    def tasks(self) -> List[Task]:
        tasks = []
        for _, queue in self.queue.items():
            tasks += queue.tasks

        return tasks


class Queue:

    def __init__(self):
        self.tasks: List[Task] = []

    def add(self, item: Task) -> None:
        self.tasks.append(item)

    def remove(self) -> Task:
        return self.tasks.pop(INITIAL_INDEX)

    def size(self) -> int:
        return len(self.tasks)

    def reverse(self) -> None:
        self.tasks.reverse()

    def clear(self) -> None:
        self.tasks.clear()

    def get(self) -> List[Task]:
        return self.tasks
