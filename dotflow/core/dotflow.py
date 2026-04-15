"""DotFlow"""

from __future__ import annotations

import os
from functools import partial
from uuid import uuid4

from dotflow.core.config import Config
from dotflow.core.task import TaskBuilder
from dotflow.core.workflow import Manager
from dotflow.logging import logger
from dotflow.utils import hostname


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

        name (Optional[str]): Human-readable label sent to the managed
            server on registration. Defaults to the machine hostname so
            runs from different hosts stay distinguishable in the
            dashboard.

    Attributes:
        workflow_id (UUID):

        name (str):

        task (List[Task]):

        start (Manager):

        schedule (Scheduler):
    """

    def __init__(
        self,
        config: Config | None = None,
        workflow_id: str | None = None,
        name: str | None = None,
    ) -> None:
        workflow_id = workflow_id or os.getenv("WORKFLOW_ID")
        self._externally_provided_id = workflow_id is not None
        self.workflow_id = workflow_id or uuid4()
        self.name = name or hostname()
        self._config = config if config else Config()
        self._manager: Manager | None = None
        self._last_run_signature: tuple = ()

        self.task = TaskBuilder(
            config=self._config,
            workflow_id=self.workflow_id,
            workflow_name=self.name,
        )

        if not self._externally_provided_id:
            self._config.server.create_workflow(workflow=self)

        self.schedule = partial(
            self._config.scheduler.start, workflow=self.start
        )

    def start(self, **kwargs) -> Manager:
        """Run the workflow once; duplicate calls return the original Manager."""
        signature = tuple(task.task_id for task in self.task.queue)
        if self._manager is not None and signature == self._last_run_signature:
            logger.warning(
                "DotFlow.start() already ran for %s; ignoring duplicate call",
                self.workflow_id,
            )
            return self._manager

        self._last_run_signature = signature
        self._manager = Manager(
            tasks=self.task.queue,
            workflow_id=self.workflow_id,
            config=self._config,
            **kwargs,
        )
        return self._manager

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
