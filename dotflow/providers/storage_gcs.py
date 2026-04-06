"""Storage GCS"""

from collections.abc import Callable
from json import dumps, loads
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.core.exception import ModuleNotFound


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
        try:
            from google.api_core.exceptions import NotFound
            from google.cloud import storage as gcs
        except ImportError:
            raise ModuleNotFound(
                module="google-cloud-storage",
                library="dotflow[gcp]",
            ) from None

        self._not_found = NotFound
        self.client = gcs.Client(project=project)
        self.bucket_obj = self.client.bucket(bucket)
        self.bucket_obj.reload()
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
        task_context = self._read(key)

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

    def _read(self, key: str) -> list:
        blob = self.bucket_obj.blob(f"{self.prefix}{key}")
        try:
            data = blob.download_as_text()
            return loads(data)
        except self._not_found:
            return []

    def _write(self, key: str, data: list) -> None:
        blob = self.bucket_obj.blob(f"{self.prefix}{key}")
        blob.upload_from_string(
            dumps(data),
            content_type="application/json",
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
