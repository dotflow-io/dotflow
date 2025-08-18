"""Status Task Type module"""

from enum import StrEnum
from typing_extensions import Literal


class StatusTaskType(StrEnum):
    """
    Import:
        You can import the **StatusTaskType** class with:

            from dotflow.core.types import StatusTaskType
    """

    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    RETRY = "Retry"
    FAILED = "Failed"

    @classmethod
    def get_symbol(cls, value: str) -> str:
        status = {
           StatusTaskType.NOT_STARTED: "⚪",
           StatusTaskType.IN_PROGRESS: "🔵",
           StatusTaskType.COMPLETED: "✅",
           StatusTaskType.PAUSED: "◼️",
           StatusTaskType.RETRY: "❗",
           StatusTaskType.FAILED: "❌"
        }
        return status.get(value)


TYPE_STATUS_TASK = Literal[
    StatusTaskType.NOT_STARTED,
    StatusTaskType.IN_PROGRESS,
    StatusTaskType.COMPLETED,
    StatusTaskType.PAUSED,
    StatusTaskType.RETRY,
    StatusTaskType.FAILED
]
