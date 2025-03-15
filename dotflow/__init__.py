"""Dotflow __init__ module."""

__version__ = "0.9.1"
__description__ = "🎲 Dotflow turns an idea into flow!"

from .core.action import Action as action
from .core.config import Config
from .core.context import Context
from .core.dotflow import DotFlow
from .core.task import Task

from .providers.storages import (
    StorageInit,
    StorageLocal
)


__all__ = [
    "action",
    "Context",
    "Config",
    "DotFlow",
    "Task",
    "StorageInit",
    "StorageLocal"
]
