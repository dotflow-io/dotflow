"""Notify ABC"""

from abc import ABC, abstractmethod
from typing import Any


class Notify(ABC):
    """Notify"""

    @abstractmethod
    def hook_status_task(self, task: Any) -> None:
        """Hook called when a task status changes."""
