"""Storage Default"""

from typing import Callable
from ctypes import cast, py_object

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageDefault(Storage):
    """Storage"""

    def post(self, key: str, context: Context) -> None:
        return None

    def get(self, key: str) -> Context:
        return Context(storage=cast(key, py_object).value)

    def key(self, task: Callable):
        return id(task.current_context)
