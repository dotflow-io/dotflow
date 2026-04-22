"""Abstract base for remote server communication."""

from abc import ABC, abstractmethod
from typing import Any


class Server(ABC):
    """Server ABC provider for sending workflow/task data remotely."""

    @abstractmethod
    def create_workflow(self, workflow: Any) -> None:
        """Register a new workflow on the remote server."""

    @abstractmethod
    def update_workflow(self, workflow: Any, status: str = "") -> None:
        """Update workflow status on the remote server."""

    @abstractmethod
    def create_task(self, task: Any) -> None:
        """Register a new task on the remote server."""

    @abstractmethod
    def update_task(self, task: Any) -> None:
        """Update task data on the remote server."""
