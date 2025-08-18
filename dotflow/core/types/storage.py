"""Storage Type module"""

from enum import StrEnum
from typing import Literal


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
