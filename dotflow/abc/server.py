"""Abstract base for remote server communication."""

from abc import ABC, abstractmethod
from typing import Any

from dotflow.constants import INITIAL_TASK_ID


class Server(ABC):
    """Server ABC provider for sending workflow and task
    data to a remote API.

    Implementations should handle HTTP communication with
    a server like dotflow-api, sending execution data
    (status, duration, errors, context) in real time.
    """

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

    def get_next_task_id(self, workflow: Any) -> int:
        """Return the next task id to use inside an existing workflow.
        """
        return INITIAL_TASK_ID
