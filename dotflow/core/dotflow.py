"""DotFlow"""

from uuid import uuid4
from functools import partial
from typing import Optional

from dotflow.core.config import Config
from dotflow.core.workflow import Manager
from dotflow.core.task import TaskBuilder


class DotFlow:
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
        config (Optional[Config]): Configuration class.

    Attributes:
        workflow_id (UUID):

        task (List[Task]):

        start (Manager):
    """

    def __init__(
            self,
            config: Optional[Config] = None
    ) -> None:
        self.workflow_id = uuid4()
        config = config if config else Config()

        self.task = TaskBuilder(
            config=config,
            workflow_id=self.workflow_id
        )

        self.start = partial(
            Manager,
            tasks=self.task.queue,
            workflow_id=self.workflow_id
        )

    def result_task(self):
        """
        Returns:
            list (List[Task]): Returns a list of Task class.
        """
        return self.task.queue

    def result_context(self):
        """
        Returns:
            list (List[Context]): Returns a list of Context class.
        """
        return [task.current_context for task in self.task.queue]

    def result_storage(self):
        """
        Returns:
            list (List[Any]): Returns a list of assorted objects.
        """
        return [task.current_context.storage for task in self.task.queue]

    def result(self):
        return self.task.result()
