"""Notify ABC"""

from abc import ABC, abstractmethod
from typing import Any


class Notify(ABC):
    """Notify"""

    @abstractmethod
    def send(self, task: Any) -> None:
        """Send"""
