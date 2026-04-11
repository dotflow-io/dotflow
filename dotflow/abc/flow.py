"""Flow ABC"""

from abc import ABC, abstractmethod
from uuid import UUID

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

    def _try_restore_checkpoint(self, task: Task):
        """Attempts to restore a checkpoint. Returns the Context if found, None otherwise."""
        if not self.resume:
            return None

        context = task.config.storage.get(
            key=task.config.storage.key(task=task)
        )

        if context.storage is None:
            return None

        task.status = TypeStatus.COMPLETED
        task.current_context = context
        self._flow_callback(task=task)

        return context
