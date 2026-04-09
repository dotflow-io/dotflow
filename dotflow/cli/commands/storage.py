"""Storage resolver for CLI commands"""

from dotflow.providers import (
    StorageDefault,
    StorageFile,
    StorageGCS,
    StorageS3,
)
from dotflow.settings import Settings as settings


class StorageResolver:
    """Resolves a storage provider instance from CLI params."""

    def __init__(self, params):
        self.params = params

    def resolve(self):
        """Returns a storage instance or None if no --storage was specified."""
        if not self.params.storage:
            return None

        resolvers = {
            "default": self._resolve_local,
            "file": self._resolve_local,
            "s3": self._resolve_s3,
            "gcs": self._resolve_gcs,
        }

        resolver = resolvers.get(self.params.storage)
        if resolver is None:
            return None

        return resolver()

    def _resolve_local(self):
        storage_cls = {"default": StorageDefault, "file": StorageFile}
        return storage_cls[self.params.storage](path=self.params.path)

    def _resolve_s3(self):
        self._require("bucket")
        return StorageS3(bucket=self.params.bucket, region=self.params.region)

    def _resolve_gcs(self):
        self._require("bucket")
        return StorageGCS(
            bucket=self.params.bucket, project=self.params.gcp_project
        )

    def _require(self, arg):
        if not getattr(self.params, arg, None):
            raise SystemExit(
                f"{settings.ERROR_ALERT} --storage {self.params.storage}"
                f" requires --{arg}"
            )
