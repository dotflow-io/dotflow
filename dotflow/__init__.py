"""Dotflow __init__ module."""

__version__ = "0.3.0"

from .core.action import Action as action
from .core.context import Context
from .core.decorators import retry  # deprecated
from .core.workflow import DotFlow


__all__ = [
    "action",
    "retry",
    "DotFlow",
    "Context"
]
