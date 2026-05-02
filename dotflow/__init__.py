"""Dotflow __init__ module."""

__version__ = "1.0.0.dev6"
__description__ = "🎲 Dotflow turns an idea into flow!"

from .core.action import Action as action
from .core.config import Config
from .core.context import Context
from .core.dotflow import DotFlow
from .core.task import Task

__all__ = ["action", "Context", "Config", "DotFlow", "Task"]
