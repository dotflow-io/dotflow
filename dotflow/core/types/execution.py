"""Execution Mode Type module"""

from enum import StrEnum
from typing import Literal


class ExecutionModeType(StrEnum):
    """
    Import:
        You can import the **ExecutionModeType** class with:

            from dotflow.core.types import ExecutionModeType
    """

    SEQUENTIAL = "sequential"
    BACKGROUND = "background"
    PARALLEL = "parallel"


TYPE_MODE_EXECUTION = Literal[
    ExecutionModeType.SEQUENTIAL,
    ExecutionModeType.BACKGROUND,
    ExecutionModeType.PARALLEL
]
