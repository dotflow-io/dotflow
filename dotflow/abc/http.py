"""HTTP ABC"""

from abc import ABC, abstractmethod
from collections.abc import Callable


class HTTPRequest(ABC):
    def __init__(self, url: str, context: Callable):
        self.url = url
        self.context = context

    @abstractmethod
    def request(
        self,
        method: str,
        body: dict,
        params: dict,
        headers: dict,
    ) -> None:
        pass
