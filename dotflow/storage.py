"""Storage module"""

from dotflow.core.exception import ModuleNotFound

from .providers.storage_file import StorageFile
from .providers.storage_init import StorageInit


class _MongoDBModuleNotFound:

    def __init__(self, *args, **kwargs):
        raise ModuleNotFound(
            module="StorageMongoDB",
            library="dotflow-mongodb"
        )


try:
    from dotflow_mongodb import StorageMongoDB
except ModuleNotFoundError:
    StorageMongoDB = _MongoDBModuleNotFound


__all__ = [
    "StorageFile",
    "StorageInit",
    "StorageMongoDB"
]
