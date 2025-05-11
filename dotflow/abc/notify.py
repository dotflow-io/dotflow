"""Notify ABC"""

from typing import Any

from abc import ABC, abstractmethod


class Notify(ABC):
    """Notify"""

    @abstractmethod
    def send(self, task: Any) -> None:
        """Send"""
