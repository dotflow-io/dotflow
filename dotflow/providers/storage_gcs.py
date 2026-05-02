"""Storage GCS"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from json import dumps, loads
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.cloud.gcp.services.gcs import GCS
from dotflow.core.context import Context


class StorageGCS(Storage):
    """
    Import:
        You can import the **StorageGCS** class directly from dotflow providers:

            from dotflow.providers import StorageGCS

    Example:
        `class` dotflow.providers.storage_gcs.StorageGCS

            from dotflow import Config
            from dotflow.providers import StorageGCS

            config = Config(
                storage=StorageGCS(
                    bucket="my-dotflow-bucket",
                    prefix="workflows/",
                    project="my-gcp-project"
                )
            )

    Args:
        bucket (str): GCS bucket name.

        prefix (str): Key prefix for all stored objects.

        project (str): GCP project ID. Defaults to ADC project.
    """

    def __init__(
        self,
        *args,
        bucket: str,
        prefix: str = "dotflow/",
        project: str = None,
        **kwargs,
    ):
        self._gcs = GCS(bucket=bucket, prefix=prefix, project=project)

    def post(
        self,
        key: str,
        context: Context,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> None:
        task_context = []

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))
        else:
            task_context.append(self._dumps(storage=context.storage))

        self._gcs.write(key=key, data=task_context)

        if fingerprint is not None:
            self._gcs.write(key=f"{key}.fingerprint", data=[fingerprint])

    def get(self, key: str) -> Context:
        task_context = self._gcs.read(key)

        if len(task_context) == 0:
            return Context()

        if len(task_context) == 1:
            return self._loads(storage=task_context[0])

        contexts = Context(storage=[])

        for context in task_context:
            contexts.storage.append(self._loads(storage=context))

        return contexts

    def delete(self, key: str) -> bool:
        existed = self._gcs.delete(key=key)
        self._gcs.delete(key=f"{key}.fingerprint")

        return existed

    def delete_prefix(self, prefix: str) -> int:
        names = self._gcs.list_keys(prefix)

        if not names:
            return 0

        self._gcs.delete_prefix(prefix)

        return sum(1 for n in names if not n.endswith(".fingerprint"))

    def list_keys(self, prefix: str) -> Iterable[str]:
        return [
            n
            for n in self._gcs.list_keys(prefix)
            if not n.endswith(".fingerprint")
        ]

    def atomic_swap(
        self,
        key: str,
        expected: Any,
        new: Any,
        ttl: int | None = None,
        fingerprint: str | None = None,
    ) -> bool:
        data, generation = self._gcs.read_with_generation(key)

        if not data:
            current_value = None
        elif len(data) == 1:
            current_value = self._loads(storage=data[0]).storage
        else:
            current_value = [self._loads(storage=d).storage for d in data]

        if current_value != expected:
            return False

        payload = new if isinstance(new, Context) else Context(storage=new)
        new_data = [self._dumps(storage=payload.storage)]

        swapped = self._gcs.write_if_generation_match(
            key=key,
            data=new_data,
            generation=generation,
        )

        if swapped and fingerprint is not None:
            self._gcs.write(key=f"{key}.fingerprint", data=[fingerprint])

        return swapped

    def key(self, task: Callable) -> str:
        return f"{task.workflow_id}-{task.task_id}"

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
