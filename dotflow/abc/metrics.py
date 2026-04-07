"""Metrics ABC"""

from abc import ABC, abstractmethod
from typing import Any


class Metrics(ABC):
    """Metrics"""

    @abstractmethod
    def workflow_started(self, workflow_id: Any, **kwargs) -> None:
        """Called when a workflow starts."""

    @abstractmethod
    def workflow_completed(self, workflow_id: Any, duration: float) -> None:
        """Called when a workflow completes successfully."""

    @abstractmethod
    def workflow_failed(self, workflow_id: Any, duration: float) -> None:
        """Called when a workflow fails."""

    @abstractmethod
    def task_completed(self, task: Any) -> None:
        """Called when a task completes successfully."""

    @abstractmethod
    def task_failed(self, task: Any) -> None:
        """Called when a task fails."""

    @abstractmethod
    def task_retried(self, task: Any) -> None:
        """Called when a task is retried."""
