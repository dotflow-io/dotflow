"""DotFlow module"""

from uuid import uuid4, UUID
from functools import partial

from typing import Callable, Union

from dotflow.abc.logs import Logs
from dotflow.abc.metrics import Metrics
from dotflow.abc.notify import Notify
from dotflow.abc.storage import Storage
from dotflow.core.plugin import Plugin

from dotflow.core.workflow import Manager
from dotflow.core.task import TaskBuilder


class DotflowInstance:

    def __init__(self, *_args, **_kwargs):
        self._plugins: Plugin = None
        self._workflow_id: UUID = None
        self._task: TaskBuilder = None
        self._add: Callable = None
        self._start: Manager = None


class DotFlow(DotflowInstance):
    """
    Import:
        You can import the **Dotflow** class directly from dotflow:

    Example:
        `class` dotflow.core.dotflow.Dotflow

            workflow = DotFlow()

    Args:
        plugins (Union[Logs, Metrics, Notify, Storage]): Plugin class.

    Attributes:
        workflow_id (UUID):

        task (TaskBuilder):

        add (Callable):

        start (Manager):
    """

    def __init__(
        self,
        plugins: Union[Logs, Metrics, Notify, Storage] = None,
    ) -> None:
        super().__init__()
        self.plugins: Plugin = plugins
        self.workflow_id: UUID = None
        self.task: TaskBuilder = None
        self.add: Callable = None
        self.start: Manager = None

    @property
    def plugins(self):
        return self._plugins

    @plugins.setter
    def plugins(self, value):
        self._plugins = Plugin()

        if value:
            self._plugins._loading_external_plugins(plugins=value)

    @property
    def workflow_id(self):
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, value):
        if not value:
            value = uuid4()
        self._workflow_id = value

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        if not value:
            value = TaskBuilder(
                plugins=self.plugins,
                workflow_id=self.workflow_id
            )
        self._task = value

    @property
    def add(self):
        return self._add

    @add.setter
    def add(self, value):
        if not value:
            value = self.task.add
        self._add = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if not value:
            value = partial(
                Manager,
                group=self.task.group,
                workflow_id=self.workflow_id
            )
        self._start = value

    def result_task(self):
        """
        Returns:
            list (List[Task]): Returns a list of Task class.
        """
        return self.task.group.tasks()

    def result_context(self):
        """
        Returns:
            list (List[Context]): Returns a list of Context class.
        """
        return [task.current_context for task in self.task.group.tasks()]

    def result_storage(self):
        """
        Returns:
            list (List[Any]): Returns a list of assorted objects.
        """
        return [task.current_context.storage for task in self.task.group.tasks()]

    def result(self):
        return self.task.result()
