"""Dotflow __init__ module."""

__version__ = "0.1.0"

from .core.action import action
from .core.executor import Executor
from .core.workflow import (
    Context,
    Task,
    Workflow
)


__all__ = [
    "action",
    "Context",
    "Executor",
    "Task",
    "Workflow"
]
