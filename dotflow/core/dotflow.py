"""DotFlow"""

from __future__ import annotations

from functools import partial
from uuid import uuid4

from dotflow.core.config import Config
from dotflow.core.task import TaskBuilder
from dotflow.core.workflow import Manager


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

        workflow_id (Optional[str]): Fixed workflow identifier for checkpoint
            resume. If not provided, a random UUID is generated.

    Attributes:
        workflow_id (UUID):

        task (List[Task]):

        start (Manager):

        schedule (Scheduler):
    """

    def __init__(
        self,
        config: Config | None = None,
        workflow_id: str | None = None,
    ) -> None:
        self.workflow_id = workflow_id or uuid4()
        self._config = config if config else Config()
        self._config.server.create_workflow(workflow=self.workflow_id)

        self.task = TaskBuilder(
            config=self._config, workflow_id=self.workflow_id
        )

        self.start = partial(
            Manager,
            tasks=self.task.queue,
            workflow_id=self.workflow_id,
            config=self._config,
        )

        self.schedule = partial(
            self._config.scheduler.start, workflow=self.start
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

    def result(self) -> dict:
        """
        Returns:
            dict: Returns the full workflow result serialized as a dictionary,
                  including workflow ID and all task schemas.
        """
        return self.task.result()
