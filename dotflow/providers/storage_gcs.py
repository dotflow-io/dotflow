"""Storage GCS"""

from collections.abc import Callable
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

    def post(self, key: str, context: Context) -> None:
        task_context = []

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))
        else:
            task_context.append(self._dumps(storage=context.storage))

        self._gcs.write(key=key, data=task_context)

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

    def key(self, task: Callable):
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
