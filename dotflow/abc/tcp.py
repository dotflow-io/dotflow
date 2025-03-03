"""TCP module"""

from abc import ABC, abstractmethod
from typing import Callable


class TCPClient(ABC):

    def __init__(self, url: str):
        self.url = url
        self.context = None

    @abstractmethod
    def sender(self, content: dict) -> None:
        pass


class TCPServer(ABC):

    def __init__(self, url: str, handler: Callable):
        self.url = url
        self.handler = handler
        self.context = None

    @abstractmethod
    async def receiver(self) -> None:
        pass

    @abstractmethod
    async def run(self) -> None:
        pass
