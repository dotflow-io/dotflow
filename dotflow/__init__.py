"""Dotflow __init__ module."""

__version__ = "0.3.0"

from .core.actions import Action as action
from .core.actions import retry  # deprecated
from .core.workflow import DotFlow
from .core.context import Context


__all__ = [
    "action",
    "retry",
    "DotFlow",
    "Context"
]
