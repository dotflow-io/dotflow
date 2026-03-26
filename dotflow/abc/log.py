"""Notify ABC"""

from abc import ABC, abstractmethod
from typing import Any


class Log(ABC):
    """Log"""

    @abstractmethod
    def info(self, task: Any) -> None:
        """Info"""

    @abstractmethod
    def error(self, task: Any) -> None:
        """Error"""
