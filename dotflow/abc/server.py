"""Server ABC"""

from abc import ABC, abstractmethod
from uuid import UUID

from dotflow.core.context import Context


class Server(ABC):

    @abstractmethod
    def ping(self) -> bool:
        pass

    @abstractmethod
    def create_task(self, id: int) -> None:
        pass

    @abstractmethod
    def create_workflow(self, id: UUID) -> None:
        pass

    @abstractmethod
    def create_context(self, context: Context) -> None:
        pass
