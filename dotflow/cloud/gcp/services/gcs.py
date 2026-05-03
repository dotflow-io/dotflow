"""GCS operations — read and write objects."""

from __future__ import annotations

from json import dumps, loads

from dotflow.cloud.core import ObjectStorage
from dotflow.core.exception import ModuleNotFound


class GCS(ObjectStorage):
    """Google Cloud Storage object storage."""

    def __init__(self, bucket: str, prefix: str = "", project: str = None):
        try:
            from google.api_core.exceptions import NotFound
            from google.cloud import storage as gcs
        except ImportError:
            raise ModuleNotFound(
                module="google-cloud-storage",
                library="dotflow[gcp]",
            ) from None

        self._not_found = NotFound
        self._client = gcs.Client(project=project)
        self._bucket = self._client.bucket(bucket)
        self._bucket.reload()
        self.prefix = prefix

    def read(self, key: str) -> list:
        """Read a JSON list from GCS. Returns empty list if key not found."""
        blob = self._bucket.blob(f"{self.prefix}{key}")
        try:
            data = blob.download_as_text()
            return loads(data)
        except self._not_found:
            return []

    def write(self, key: str, data: list) -> None:
        """Write a JSON list to GCS."""
        blob = self._bucket.blob(f"{self.prefix}{key}")
        blob.upload_from_string(
            dumps(data),
            content_type="application/json",
        )

    def delete(self, key: str) -> bool:
        """Delete a single blob."""
        blob = self._bucket.blob(f"{self.prefix}{key}")

        try:
            blob.delete()
            return True
        except self._not_found:
            return False

    def read_with_generation(self, key: str) -> tuple[list, int | None]:
        """Return (data, generation). Generation is None when missing."""
        blob = self._bucket.blob(f"{self.prefix}{key}")

        try:
            data = blob.download_as_text()
            return loads(data), blob.generation
        except self._not_found:
            return [], None

    def write_if_generation_match(
        self, key: str, data: list, generation: int | None
    ) -> bool:
        """Conditional upload. Returns False on precondition failure."""
        from google.api_core.exceptions import PreconditionFailed

        blob = self._bucket.blob(f"{self.prefix}{key}")
        precondition = generation if generation is not None else 0

        try:
            blob.upload_from_string(
                dumps(data),
                content_type="application/json",
                if_generation_match=precondition,
            )
            return True
        except PreconditionFailed:
            return False

    def list_keys(self, sub_prefix: str) -> list[str]:
        """Return blob names starting with sub_prefix."""
        full_prefix = f"{self.prefix}{sub_prefix}"
        offset = len(self.prefix)

        return [
            blob.name[offset:]
            for blob in self._client.list_blobs(
                self._bucket, prefix=full_prefix
            )
        ]

    def delete_prefix(self, sub_prefix: str) -> None:
        """Delete every blob whose name starts with prefix + sub_prefix.

        Empty ``sub_prefix`` is rejected to avoid accidentally wiping
        the entire bucket prefix.
        """
        if not sub_prefix:
            raise ValueError("delete_prefix requires a non-empty sub_prefix")

        full_prefix = f"{self.prefix}{sub_prefix}"

        for blob in self._client.list_blobs(self._bucket, prefix=full_prefix):
            blob.delete()
