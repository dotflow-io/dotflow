"""Storage S3"""

from collections.abc import Callable
from json import dumps, loads
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.core.exception import ModuleNotFound


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
        try:
            import boto3
        except ImportError:
            raise ModuleNotFound(
                module="boto3", library="dotflow[aws]"
            ) from None

        self.s3 = boto3.client("s3", region_name=region)
        self.bucket = bucket
        self.prefix = prefix

    def post(self, key: str, context: Context) -> None:
        task_context = []

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))
        else:
            task_context.append(self._dumps(storage=context.storage))

        self._write(key=key, data=task_context)

    def get(self, key: str) -> Context:
        task_context = self._read_existing(key)

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

    def _read_existing(self, key: str) -> list:
        try:
            response = self.s3.get_object(
                Bucket=self.bucket,
                Key=f"{self.prefix}{key}",
            )
            data = response["Body"].read().decode("utf-8")
            return loads(data)
        except self.s3.exceptions.NoSuchKey:
            return []

    def _write(self, key: str, data: list) -> None:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=f"{self.prefix}{key}",
            Body=dumps(data),
            ContentType="application/json",
        )

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
