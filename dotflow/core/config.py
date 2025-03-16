"""Config module"""

from dotflow.abc.storage import Storage
from dotflow.providers.storage_default import StorageDefault


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow import Config
            from dotflow.storage import StorageDefault

    Example:
        `class` dotflow.core.config.Config

            config = Config(storage=StorageDefault)

    Args:
        storage (Storage): Type of the storage.

    Attributes:
        storage (Storage):
    """

    def __init__(self, storage: Storage = StorageDefault()) -> None:
        self.storage = storage
