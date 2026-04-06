"""Scheduler ABC"""

from abc import ABC, abstractmethod
from collections.abc import Callable


class Scheduler(ABC):
    """Scheduler"""

    @abstractmethod
    def start(self, workflow: Callable, **kwargs) -> None:
        """Start the scheduler loop with the given workflow execution."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the scheduler loop gracefully."""
