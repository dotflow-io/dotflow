"""Dotflow __init__ module."""

__version__ = "0.9.0"
__description__ = "🎲 Dotflow turns an idea into flow!"

from .core.config import Config
from .core.action import Action as action
from .core.context import Context
from .core.dotflow import DotFlow
from .core.task import Task
from .core.decorators import retry  # deprecated


__all__ = [
    "action",
    "retry",
    "DotFlow",
    "Context",
    "Config",
    "Task"
]
