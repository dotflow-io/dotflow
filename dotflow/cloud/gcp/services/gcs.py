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
