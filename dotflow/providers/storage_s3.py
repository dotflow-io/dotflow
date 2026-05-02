"""Storage S3"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from json import dumps, loads
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.cloud.aws.services.s3 import S3
from dotflow.core.context import Context


class StorageS3(Storage):
    """
    Import:
        You can import the **StorageS3** class directly from dotflow providers:

            from dotflow.providers import StorageS3

    Example:
        `class` dotflow.providers.storage_s3.StorageS3

            from dotflow import Config
            from dotflow.providers import StorageS3

            config = Config(
                storage=StorageS3(
                    bucket="my-dotflow-bucket",
                    prefix="workflows/",
                    region="us-east-1"
                )
            )

    Args:
        bucket (str): S3 bucket name.

        prefix (str): Key prefix for all stored objects.

        region (str): AWS region name. Defaults to boto3 default.
    """

    def __init__(
        self,
        *args,
        bucket: str,
        prefix: str = "dotflow/",
        region: str = None,
        **kwargs,
    ):
        self._s3 = S3(bucket=bucket, prefix=prefix, region=region)

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

        self._s3.write(key=key, data=task_context)

        if fingerprint is not None:
            self._s3.write(key=f"{key}.fingerprint", data=[fingerprint])

    def get(self, key: str) -> Context:
        task_context = self._s3.read(key)

        if len(task_context) == 0:
            return Context()

        if len(task_context) == 1:
            return self._loads(storage=task_context[0])

        contexts = Context(storage=[])

        for context in task_context:
            contexts.storage.append(self._loads(storage=context))

        return contexts

    def delete(self, key: str) -> bool:
        existed = self._s3.delete(key=key)
        self._s3.delete(key=f"{key}.fingerprint")

        return existed

    def delete_prefix(self, prefix: str) -> int:
        names = self._s3.list_keys(prefix)

        if not names:
            return 0

        self._s3.delete_prefix(prefix)

        return sum(1 for n in names if not n.endswith(".fingerprint"))

    def list_keys(self, prefix: str) -> Iterable[str]:
        return [
            n
            for n in self._s3.list_keys(prefix)
            if not n.endswith(".fingerprint")
        ]

    def atomic_swap(self, key: str, expected: Any, new: Any) -> bool:
        current = self.get(key)
        current_value = (
            current.storage if isinstance(current, Context) else None
        )

        if current_value != expected:
            return False

        self.delete(key)
        payload = new if isinstance(new, Context) else Context(storage=new)
        self.post(key=key, context=payload)

        return True

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
