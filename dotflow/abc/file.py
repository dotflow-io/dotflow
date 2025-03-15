"""File ABC"""

from abc import ABC, abstractmethod


class FileClient(ABC):

    @abstractmethod
    @classmethod
    def write(
        self,
        path: str,
        content: str,
        mode: str,
        encoding: str
    ) -> None:
        pass

    @abstractmethod
    @classmethod
    def read(self, path: str) -> str:
        pass
