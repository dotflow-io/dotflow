"""Storage ABC"""

from abc import ABC, abstractmethod
from collections.abc import Callable

from dotflow.core.context import Context


class Storage(ABC):
    """Storage"""

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, key: str, context: Context) -> None:
        """Post context somewhere"""

    @abstractmethod
    def get(self, key: str) -> Context:
        """Get context somewhere"""

    @abstractmethod
    def key(self, task: Callable):
        """Function that returns a key to get and post storage"""

    @abstractmethod
    def clear(self, workflow_id: str) -> None:
        """Remove every persisted entry under ``workflow_id``.

        Used by the input-fingerprint reset path when
        ``on_input_change='reset'``.
        """
