"""Storage ABC"""

from abc import ABC, abstractmethod

from dotflow.core.context import Context


class Storage(ABC):
    """Storage"""

    @abstractmethod
    def post(self, key: str, context: Context) -> None:
        """Post context"""

    @abstractmethod
    def get(self, key: str) -> Context:
        """Get context"""
