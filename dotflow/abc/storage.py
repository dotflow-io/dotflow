"""Storage ABC"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Any

from dotflow.core.context import Context


class Storage(ABC):
    """Storage"""

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(
        self,
        key: str,
        context: Context,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        """Persist context under key."""

    @abstractmethod
    def get(self, key: str) -> Context:
        """Return stored context or empty Context()."""

    @abstractmethod
    def key(self, task: Callable) -> str:
        """Storage key for task."""

    def clear(self, workflow_id: str) -> None:
        """Remove every entry under workflow_id.

        Default implementation delegates to ``delete_prefix``. External
        subclasses may override directly.
        """
        self.delete_prefix(f"{workflow_id}-")

    def delete(self, key: str) -> bool:
        """Remove key. Returns True when present.

        Optional in 1.x. Becomes abstract in 2.0.
        """
        raise NotImplementedError

    def delete_prefix(self, prefix: str) -> int:
        """Remove keys starting with prefix. Returns count.

        Optional in 1.x. Becomes abstract in 2.0.
        """
        raise NotImplementedError

    def list_keys(self, prefix: str) -> Iterable[str]:
        """Iterate keys starting with prefix.

        Optional in 1.x. Becomes abstract in 2.0.
        """
        raise NotImplementedError

    def atomic_swap(
        self,
        key: str,
        expected: Any,
        new: Any,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> bool:
        """Replace value when current equals expected.

        Optional in 1.x. Becomes abstract in 2.0.
        """
        raise NotImplementedError
