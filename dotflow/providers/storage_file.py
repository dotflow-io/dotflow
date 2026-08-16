"""Storage File"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Iterable
from json import dumps, loads
from pathlib import Path
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.settings import Settings as settings
from dotflow.utils import read_file, write_file


class StorageFile(Storage):
    """File-backed storage."""

    def __init__(self, *args, path: str = settings.START_PATH, **kwargs):
        self.path = Path(path, "tasks")
        self.path.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def post(
        self,
        key: str,
        context: Context,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        with self._lock:
            task_context = []

            if Path(self.path, key).exists():
                data = read_file(path=Path(self.path, key))

                if isinstance(data, list):
                    task_context = data

            if isinstance(context.storage, list):
                for item in context.storage:
                    if isinstance(item, Context):
                        task_context.append(self._dumps(storage=item.storage))
            else:
                task_context.append(self._dumps(storage=context.storage))

            write_file(path=Path(self.path, key), content=task_context)

            meta = {}

            if fingerprint is not None:
                meta["fingerprint"] = fingerprint

            if ttl is not None:
                meta["expires_at"] = time.time() + ttl

            if meta:
                self._write_meta(key=key, meta=meta)

    def get(self, key: str) -> Context:
        with self._lock:
            if self._is_expired(key):
                self.delete(key)

                return Context()

            task_context = []

            if Path(self.path, key).exists():
                data = read_file(path=Path(self.path, key))

                if isinstance(data, list):
                    task_context = data

            if not task_context:
                return Context()

            if len(task_context) == 1:
                return self._loads(storage=task_context[0])

            contexts = Context(storage=[])

            for context in task_context:
                contexts.storage.append(self._loads(storage=context))

            return contexts

    def delete(self, key: str) -> bool:
        with self._lock:
            target = Path(self.path, key)
            existed = target.exists()

            target.unlink(missing_ok=True)
            Path(self.path, f"{key}.meta").unlink(missing_ok=True)

            return existed

    def delete_prefix(self, prefix: str) -> int:
        with self._lock:
            removed = 0

            for entry in self.path.iterdir():
                if not entry.is_file():
                    continue

                if entry.name.endswith(".meta"):
                    continue

                if not entry.name.startswith(prefix):
                    continue

                entry.unlink(missing_ok=True)
                Path(self.path, f"{entry.name}.meta").unlink(missing_ok=True)
                removed += 1

            return removed

    def list_keys(self, prefix: str) -> Iterable[str]:
        with self._lock:
            names = []

            for entry in self.path.iterdir():
                if not entry.is_file():
                    continue

                if entry.name.endswith(".meta"):
                    continue

                if not entry.name.startswith(prefix):
                    continue

                if self._is_expired(entry.name):
                    self.delete(entry.name)
                    continue

                names.append(entry.name)

            return names

    def atomic_swap(
        self,
        key: str,
        expected: Any,
        new: Any,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> bool:
        with self._lock:
            current = self.get(key)
            current_value = (
                current.storage if isinstance(current, Context) else None
            )

            if current_value != expected:
                return False

            self.delete(key)
            payload = new if isinstance(new, Context) else Context(storage=new)
            self.post(
                key=key,
                context=payload,
                ttl=ttl,
                fingerprint=fingerprint,
            )

            return True

    def key(self, task: Callable) -> str:
        return f"{task.workflow_id}-{task.task_id}.json"

    def _write_meta(self, key: str, meta: dict) -> None:
        Path(self.path, f"{key}.meta").write_text(dumps(meta))

    def _read_meta(self, key: str) -> dict:
        meta_path = Path(self.path, f"{key}.meta")

        if not meta_path.exists():
            return {}

        try:
            return loads(meta_path.read_text())
        except Exception:
            return {}

    def _is_expired(self, key: str) -> bool:
        meta = self._read_meta(key=key)
        expires_at = meta.get("expires_at")

        if expires_at is None:
            return False

        return time.time() >= expires_at

    def _loads(self, storage: Any) -> Context:
        try:
            return Context(storage=loads(storage))
        except Exception:
            return Context(storage=storage)

    def _dumps(self, storage: Any) -> str:
        try:
            return dumps(storage)
        except TypeError:
            return str(storage)
