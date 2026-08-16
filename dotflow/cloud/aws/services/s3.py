"""S3 operations — read and write objects."""

from __future__ import annotations

from json import dumps, loads

from dotflow.cloud.core import ObjectStorage
from dotflow.core.exception import ModuleNotFound

_PRECONDITION_CODES = {
    "PreconditionFailed",
    "ConditionalRequestConflict",
}


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

    def delete(self, key: str) -> bool:
        """Delete a single object."""
        from botocore.exceptions import ClientError

        full_key = f"{self.prefix}{key}"

        try:
            self._s3.head_object(Bucket=self.bucket, Key=full_key)
        except ClientError as error:
            code = error.response.get("Error", {}).get("Code")

            if code in ("404", "NoSuchKey", "NotFound"):
                return False

            raise

        self._s3.delete_object(Bucket=self.bucket, Key=full_key)

        return True

    def read_with_etag(self, key: str) -> tuple[list, str | None]:
        """Return (data, etag). Etag is None when key is missing."""
        try:
            response = self._s3.get_object(
                Bucket=self.bucket,
                Key=f"{self.prefix}{key}",
            )
            data = response["Body"].read().decode("utf-8")

            return loads(data), response.get("ETag")
        except self._s3.exceptions.NoSuchKey:
            return [], None

    def write_if_match(self, key: str, data: list, etag: str | None) -> bool:
        """Conditional PutObject. Returns False on precondition failure."""
        from botocore.exceptions import ClientError

        kwargs = {
            "Bucket": self.bucket,
            "Key": f"{self.prefix}{key}",
            "Body": dumps(data),
            "ContentType": "application/json",
        }

        if etag is None:
            kwargs["IfNoneMatch"] = "*"
        else:
            kwargs["IfMatch"] = etag

        try:
            self._s3.put_object(**kwargs)
            return True
        except ClientError as error:
            code = error.response.get("Error", {}).get("Code")

            if code in _PRECONDITION_CODES:
                return False

            raise

    def list_keys(self, sub_prefix: str) -> list[str]:
        """Return keys starting with sub_prefix."""
        full_prefix = f"{self.prefix}{sub_prefix}"
        paginator = self._s3.get_paginator("list_objects_v2")
        names = []
        offset = len(self.prefix)

        for page in paginator.paginate(Bucket=self.bucket, Prefix=full_prefix):
            for item in page.get("Contents", []):
                names.append(item["Key"][offset:])

        return names

    def delete_prefix(self, sub_prefix: str) -> None:
        """Delete every object whose key starts with prefix + sub_prefix.

        Empty ``sub_prefix`` is rejected to avoid accidentally wiping
        the entire bucket prefix.
        """
        if not sub_prefix:
            raise ValueError("delete_prefix requires a non-empty sub_prefix")

        full_prefix = f"{self.prefix}{sub_prefix}"
        paginator = self._s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=self.bucket, Prefix=full_prefix):
            objects = [
                {"Key": item["Key"]} for item in page.get("Contents", [])
            ]
            if not objects:
                continue
            self._s3.delete_objects(
                Bucket=self.bucket,
                Delete={"Objects": objects},
            )
