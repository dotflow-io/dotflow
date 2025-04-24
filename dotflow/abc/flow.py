"""Flow ABC"""

from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from dotflow.core.task import Task


class Flow(ABC):

    def __init__(
            self,
            tasks: List[Task],
            workflow_id: UUID,
            ignore: bool
    ) -> None:
        self.queue = None
        self.tasks = tasks
        self.workflow_id = workflow_id
        self.ignore = ignore

        self.setup()
        self.run()

    @abstractmethod
    def setup(self) -> None:
        self.queue = []

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        return self.queue

    @abstractmethod
    def internal_callback(self, task: Task) -> None:
        self.queue.append(task)

    @abstractmethod
    def run(self) -> None:
        return None
