"""DotFlow module"""

from uuid import uuid4, UUID
from functools import partial

from typing import Callable, Optional

from dotflow.core.config import Config
from dotflow.core.workflow import Manager
from dotflow.core.task import TaskBuilder
from dotflow.utils.tools import start_and_validate_instance


class DotflowInstance:

    def __init__(self, *_args, **_kwargs):
        self._config: Config = None
        self._workflow_id: UUID = None
        self._task: TaskBuilder = None
        self._add: Callable = None
        self._start: Manager = None


class DotFlow(DotflowInstance):
    """
    Import:
        You can import the **Dotflow** class directly from dotflow:

            from dotflow import DotFlow, Config
            from dotflow.providers import StorageFile

    Example:
        `class` dotflow.core.dotflow.Dotflow

            config = Config(
                storage=StorageFile()
            )

            workflow = DotFlow(config=config)

    Args:
        config (Optional[Config]): Config class.

    Attributes:
        workflow_id (UUID):

        task (TaskBuilder):

        add (Callable):

        start (Manager):
    """

    def __init__(self, config: Optional[Config] = Config) -> None:
        super().__init__()
        self.config: Config = config
        self.workflow_id: UUID = None
        self.task: TaskBuilder = None
        self.add: Callable = None
        self.start: Manager = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if not value:
            value = Config()

        self._config = start_and_validate_instance(value, Config)

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
                config=self.config,
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
