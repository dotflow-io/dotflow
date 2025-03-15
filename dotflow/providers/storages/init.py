"""Init"""

from ctypes import cast, py_object

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageInit(Storage):
    """Storage"""

    def post(self, key: str, context: Context) -> None:
        """Post context"""

    def get(self, key: str) -> Context:
        """Get context"""
        return Context(
            storage=cast(key, py_object).value
        )
