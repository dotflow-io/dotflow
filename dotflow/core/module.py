"""Task module"""

import sys

from importlib.util import (
    spec_from_file_location as file_location,
    module_from_spec
)

from typing import Any

from dotflow.core.exception import ImportModuleError


class Module:

    def __new__(cls, value: Any):
        if isinstance(value, str):
            value = cls.import_module(value)
        return value

    @classmethod
    def import_module(cls, value: str):
        spec = file_location(value, cls._get_path(value))
        module = module_from_spec(spec)

        sys.modules[module] = module
        spec.loader.exec_module(module)

        if hasattr(module, cls._get_name(value)):
            return getattr(module, cls._get_name(value))

        raise ImportModuleError(
            module=value
        )

    @classmethod
    def _get_name(cls, value: str):
        return value.split(".")[-1:][0]

    @classmethod
    def _get_path(cls, value: str):
        return f"{'/'.join(value.split('.')[:-1])}.py"
