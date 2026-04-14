"""Task module"""

import importlib
from typing import Any

from dotflow.core.exception import ImportModuleError


class Module:
    def __new__(cls, value: Any):
        if isinstance(value, str):
            value = cls.import_module(value)
        return value

    @classmethod
    def import_module(cls, value: str):
        separator = ":" if ":" in value else "."
        module_path, _, attr_name = value.rpartition(separator)

        if not module_path:
            raise ImportModuleError(module=value)

        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            raise ImportModuleError(module=value) from None

        if hasattr(module, attr_name):
            return getattr(module, attr_name)

        raise ImportModuleError(module=value)
