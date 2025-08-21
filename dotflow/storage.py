"""Storage module"""

from dotflow.core.exception import ModuleNotFound

from .plugins.storage import StorageHandler
from .providers.storage_file import StorageFile


class _MongoDBModuleNotFound:

    def __init__(self, *args, **kwargs):
        raise ModuleNotFound(module="StorageMongoDB", library="dotflow-mongodb")


try:
    from dotflow_mongodb import StorageMongoDB  # type: ignore
except ModuleNotFoundError:
    StorageMongoDB = _MongoDBModuleNotFound


__all__ = ["StorageHandler", "StorageFile", "StorageMongoDB"]
