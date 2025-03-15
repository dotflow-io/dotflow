"""Config module"""

from dotflow.abc.storage import Storage
from dotflow.providers.storages import StorageInit


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow.core.config import Config

    Example:
        `class` dotflow.core.config.Config

            config = Config(storage=StorageLocal)

    Args:
        storage (Storage): Type of the storage.

    Attributes:
        storage (Storage):
    """

    def __init__(self, storage: Storage = None) -> None:
        self.storage = storage if bool(storage) else StorageInit()
