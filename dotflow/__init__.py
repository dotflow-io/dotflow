"""Dotflow __init__ module."""

__version__ = "0.13.1"
__description__ = "🎲 Dotflow turns an idea into flow!"

from .core.action import Action as action
from .core.context import Context
from .core.dotflow import DotFlow
from .core.task import Task


__all__ = ["action", "Context", "DotFlow", "Task"]
