"""Notify ABC"""

from typing import Any

from abc import ABC, abstractmethod


class Log(ABC):
    """Log"""

    @abstractmethod
    def info(self, task: Any) -> None:
        """Info"""

    @abstractmethod
    def error(self, task: Any) -> None:
        """Error"""
