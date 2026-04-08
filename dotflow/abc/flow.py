"""Flow ABC"""

from abc import ABC, abstractmethod
from uuid import UUID

from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.types import TypeStatus


class Flow(ABC):
    def __init__(
        self,
        tasks: list[Task],
        workflow_id: UUID,
        ignore: bool,
        groups: dict[str, list[Task]],
        resume: bool = False,
    ) -> None:
        self.queue = None
        self.tasks = tasks
        self.workflow_id = workflow_id
        self.ignore = ignore
        self.groups = groups
        self.resume = resume

        self.setup_queue()
        self.run()

    @abstractmethod
    def setup_queue(self) -> None:
        self.queue = []

    @abstractmethod
    def get_tasks(self) -> list[Task]:
        return self.queue

    @abstractmethod
    def _flow_callback(self, task: Task) -> None:
        self.queue.append(task)

    @abstractmethod
    def run(self) -> None:
        return None

    def _has_checkpoint(self, task: Task) -> bool:
        if not self.resume:
            return False

        context = task.config.storage.get(key=task.config.storage.key(task=task))

        return context.storage is not None

    def _restore_checkpoint(self, task: Task) -> Context:
        previous_context = task.config.storage.get(
            key=task.config.storage.key(task=task)
        )

        task.status = TypeStatus.COMPLETED
        task.current_context = previous_context
        self._flow_callback(task=task)

        return previous_context
