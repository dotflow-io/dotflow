"""Storage Default"""

from collections.abc import Callable

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageDefault(Storage):
    """In-memory storage using a dictionary."""

    def __init__(self):
        self._store: dict[str, Context] = {}

    def post(self, key: str, context: Context) -> None:
        self._store[key] = context

    def get(self, key: str) -> Context:
        return self._store.get(key, Context())

    def key(self, task: Callable) -> str:
        return f"{task.workflow_id}-{task.task_id}"

    def clear(self, workflow_id: str) -> None:
        prefix = f"{workflow_id}"
        stale = [k for k in self._store if k.startswith(prefix)]

        for key in stale:
            del self._store[key]
