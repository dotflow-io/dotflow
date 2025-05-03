"""Flow ABC"""

from abc import ABC, abstractmethod
from uuid import UUID
from typing import Dict, List

from dotflow.core.task import Task


class Flow(ABC):

    def __init__(
            self,
            tasks: List[Task],
            workflow_id: UUID,
            ignore: bool,
            groups: Dict[str, List[Task]]
    ) -> None:
        self.queue = None
        self.tasks = tasks
        self.workflow_id = workflow_id
        self.ignore = ignore
        self.groups = groups

        self.setup_queue()
        self.run()

    @abstractmethod
    def setup_queue(self) -> None:
        self.queue = []

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        return self.queue

    @abstractmethod
    def _flow_callback(self, task: Task) -> None:
        self.queue.append(task)

    @abstractmethod
    def run(self) -> None:
        return None
