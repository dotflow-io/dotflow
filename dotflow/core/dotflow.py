"""DotFlow"""

from uuid import uuid4
from functools import partial

from dotflow.core.config import Config
from dotflow.core.workflow import Workflow
from dotflow.core.task import TaskBuilder


class DotFlow:

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
            id=self.workflow_id
        )

    def result_task(self):
        return self.task.queu

    def result_context(self):
        return [task.current_context for task in self.task.queu]

    def result_storage(self):
        return [task.current_context.storage for task in self.task.queu]
