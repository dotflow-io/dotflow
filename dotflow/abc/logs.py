"""Logs ABC"""

from abc import ABC, abstractmethod


class Logs(ABC):
    """Logs"""

    group = "logs"  # Do not remove

    def __init__(self, *_args, **_kwargs):
        """Init not implemented."""
        self.client = None

    @abstractmethod
    def on_workflow_status_change(self, workflow_object) -> None:
        pass

    @abstractmethod
    def on_task_status_change(self, task_object) -> None:
        pass

    @abstractmethod
    def on_status_failed(self, task_object) -> None:
        pass

    @abstractmethod
    def when_context_assigned(self, task_objetc) -> None:
        pass
