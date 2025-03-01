"""DotFlow"""

from functools import partial

from dotflow.core.workflow import Workflow
from dotflow.core.task import TaskBuilder


class DotFlow:

    def __init__(self) -> None:
        self.task = TaskBuilder()
        self.start = partial(Workflow, self.task.queu)

    def result_task(self):
        return self.task.queu

    def result_context(self):
        return [task.current_context for task in self.task.queu]

    def result_storage(self):
        return [task.current_context.storage for task in self.task.queu]
