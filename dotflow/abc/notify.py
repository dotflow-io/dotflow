"""Notify ABC"""

from typing import Dict

from abc import ABC, abstractmethod


class Notify(ABC):
    """Notify"""

    @abstractmethod
    def send(self, task: Dict[str, any]) -> None:
        """Send task"""
