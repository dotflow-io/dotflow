"""DotFlow"""

from uuid import uuid4
from functools import partial

from dotflow.core.config import Config
from dotflow.core.workflow import Workflow
from dotflow.core.task import TaskBuilder


class DotFlow:
    """
    Import:
        You can import the **Dotflow** class directly from dotflow:

            from dotflow import DotFlow, Config
            from dotflow.storage import StorageFile

    Example:
        `class` dotflow.core.dotflow.Dotflow

            config = Config(
                storage=StorageFile()
            )

            workflow = DotFlow(config=config)

    Args:
        config (Config): Configuration class.

    Attributes:
        workflow_id (UUID):

        task (List[Task]):

        start (Workflow):
    """

    def __init__(
            self,
            config: Config = Config()
    ) -> None:
        self.workflow_id = uuid4()

        self.task = TaskBuilder(
            config=config,
            workflow_id=self.workflow_id
        )

        self.start = partial(
            Workflow,
            tasks=self.task.queu,
            workflow_id=self.workflow_id
        )

    def result_task(self):
        """
        Returns:
            list (List[Task]): Returns a list of Task class.
        """
        return self.task.queu

    def result_context(self):
        """
        Returns:
            list (List[Context]): Returns a list of Context class.
        """
        return [task.current_context for task in self.task.queu]

    def result_storage(self):
        """
        Returns:
            list (List[Any]): Returns a list of assorted objects.
        """
        return [task.current_context.storage for task in self.task.queu]
