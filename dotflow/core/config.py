"""Config module"""

from dotflow.abc.storage import Storage
from dotflow.providers.storage_init import StorageInit


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow import Config, StorageInit

    Example:
        `class` dotflow.core.config.Config

            config = Config(storage=StorageInit)

    Args:
        storage (Storage): Type of the storage.

    Attributes:
        storage (Storage):
    """

    def __init__(self, storage: Storage = StorageInit()) -> None:
        self.storage = storage
