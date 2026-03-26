"""Abstract base for optional remote API persistence."""

from abc import ABC, abstractmethod
from typing import Any


class Api(ABC):
    """Api"""

    @abstractmethod
    def create_workflow(self, workflow: Any) -> None:
        """Create workflow"""

    @abstractmethod
    def update_workflow(self, workflow: Any) -> None:
        """Update workflow"""

    @abstractmethod
    def create_task(self, task: Any) -> None:
        """Create task"""

    @abstractmethod
    def update_task(self, task: Any) -> None:
        """Update task"""
