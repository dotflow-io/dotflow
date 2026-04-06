"""Type Storage mode"""

from typing import Annotated

from typing_extensions import Doc


class TypeStorage:
    """
    Import:
        You can import the **TypeStorage** class with:

            from dotflow.core.types import TypeStorage
    """

    DEFAULT: Annotated[str, Doc("Default storage.")] = "default"
    FILE: Annotated[str, Doc("File storage.")] = "file"
    S3: Annotated[str, Doc("AWS S3 storage.")] = "s3"
    GCS: Annotated[str, Doc("Google Cloud Storage.")] = "gcs"
