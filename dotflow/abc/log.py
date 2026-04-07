"""Log ABC"""

from abc import ABC, abstractmethod


class Log(ABC):
    """Log"""

    @abstractmethod
    def info(self, **kwargs) -> None:
        """Info"""

    @abstractmethod
    def error(self, **kwargs) -> None:
        """Error"""

    def warning(self, **kwargs) -> None:
        """Warning"""

    def debug(self, **kwargs) -> None:
        """Debug"""
