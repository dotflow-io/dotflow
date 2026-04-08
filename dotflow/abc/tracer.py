"""Tracer ABC"""

from abc import ABC, abstractmethod
from typing import Any


class Tracer(ABC):
    """Tracer"""

    @abstractmethod
    def start_workflow(self, workflow_id: Any, **kwargs) -> None:
        """Called when a workflow starts execution."""

    @abstractmethod
    def end_workflow(self, workflow_id: Any, **kwargs) -> None:
        """Called when a workflow finishes execution."""

    @abstractmethod
    def start_task(self, task: Any) -> None:
        """Called when a task starts execution."""

    @abstractmethod
    def end_task(self, task: Any) -> None:
        """Called when a task finishes execution."""
