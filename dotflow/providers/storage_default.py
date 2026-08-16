"""Storage Default"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Iterable
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageDefault(Storage):
    """In-memory storage."""

    def __init__(self):
        self._store: dict[str, Context] = {}
        self._fingerprints: dict[str, str] = {}
        self._expirations: dict[str, float] = {}
        self._lock = threading.RLock()

    def post(
        self,
        key: str,
        context: Context,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        with self._lock:
            self._store[key] = context

            if fingerprint is not None:
                self._fingerprints[key] = fingerprint

            if ttl is not None:
                self._expirations[key] = time.monotonic() + ttl
            else:
                self._expirations.pop(key, None)

    def get(self, key: str) -> Context:
        with self._lock:
            self._evict_if_expired(key)

            return self._store.get(key, Context())

    def delete(self, key: str) -> bool:
        with self._lock:
            existed = key in self._store
            self._store.pop(key, None)
            self._fingerprints.pop(key, None)
            self._expirations.pop(key, None)

            return existed

    def delete_prefix(self, prefix: str) -> int:
        with self._lock:
            stale = [k for k in self._store if k.startswith(prefix)]

            for key in stale:
                self._store.pop(key, None)
                self._fingerprints.pop(key, None)
                self._expirations.pop(key, None)

            return len(stale)

    def list_keys(self, prefix: str) -> Iterable[str]:
        with self._lock:
            for key in list(self._store):
                self._evict_if_expired(key)

            return [k for k in self._store if k.startswith(prefix)]

    def atomic_swap(
        self,
        key: str,
        expected: Any,
        new: Any,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> bool:
        with self._lock:
            current = self._store.get(key)
            current_value = (
                current.storage if isinstance(current, Context) else current
            )

            if current_value != expected:
                return False

            payload = new if isinstance(new, Context) else Context(storage=new)
            self._store[key] = payload
            self._fingerprints.pop(key, None)
            self._expirations.pop(key, None)

            if fingerprint is not None:
                self._fingerprints[key] = fingerprint

            if ttl is not None:
                self._expirations[key] = time.monotonic() + ttl

            return True

    def key(self, task: Callable) -> str:
        return f"{task.workflow_id}-{task.task_id}"

    def _evict_if_expired(self, key: str) -> None:
        expiry = self._expirations.get(key)

        if expiry is None:
            return

        if time.monotonic() < expiry:
            return

        self._store.pop(key, None)
        self._fingerprints.pop(key, None)
        self._expirations.pop(key, None)
