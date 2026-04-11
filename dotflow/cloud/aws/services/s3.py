"""S3 operations — read and write objects."""

from __future__ import annotations

from json import dumps, loads

from dotflow.cloud.core import ObjectStorage
from dotflow.core.exception import ModuleNotFound


class S3(ObjectStorage):
    """Amazon S3 object storage."""

    def __init__(self, bucket: str, prefix: str = "", region: str = None):
        try:
            import boto3
        except ImportError:
            raise ModuleNotFound(
                module="boto3", library="dotflow[aws]"
            ) from None

        self._s3 = boto3.client("s3", region_name=region)
        self.bucket = bucket
        self.prefix = prefix

        self._s3.head_bucket(Bucket=self.bucket)

    def read(self, key: str) -> list:
        """Read a JSON list from S3. Returns empty list if key not found."""
        try:
            response = self._s3.get_object(
                Bucket=self.bucket,
                Key=f"{self.prefix}{key}",
            )
            data = response["Body"].read().decode("utf-8")
            return loads(data)
        except self._s3.exceptions.NoSuchKey:
            return []

    def write(self, key: str, data: list) -> None:
        """Write a JSON list to S3."""
        self._s3.put_object(
            Bucket=self.bucket,
            Key=f"{self.prefix}{key}",
            Body=dumps(data),
            ContentType="application/json",
        )
