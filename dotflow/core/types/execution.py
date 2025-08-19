"""Execution Mode Type module"""

from typing import Literal

from dotflow.core.types.enum import StrEnum


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
