"""Storage Type module"""

from typing import Literal

from dotflow.core.types.enum import StrEnum


class StorageType(StrEnum):
    """
    Import:
        You can import the **StorageType** class with:

            from dotflow.core.types import StorageType
    """

    DEFAULT = "default"
    FILE = "file"


STORAGE_TYPE = Literal[
    StorageType.DEFAULT,
    StorageType.FILE
]
