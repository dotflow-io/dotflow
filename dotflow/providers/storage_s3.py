"""Storage S3"""

from collections.abc import Callable
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

    def post(self, key: str, context: Context) -> None:
        task_context = []

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))
        else:
            task_context.append(self._dumps(storage=context.storage))

        self._s3.write(key=key, data=task_context)

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

    def key(self, task: Callable):
        return f"{task.workflow_id}-{task.task_id}"

    def clear(self, workflow_id: str) -> None:
        self._s3.delete_prefix(f"{workflow_id}")

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
