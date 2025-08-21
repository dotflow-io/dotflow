"""Status Task Type module"""

from typing_extensions import Literal

from dotflow.core.types.enum import StrEnum


class StatusTaskType(StrEnum):
    """
    Import:
        You can import the **StatusTaskType** class with:

            from dotflow.core.types import StatusTaskType
    """

    IN_QUEUE = "In queue"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    RETRY = "Retry"
    FAILED = "Failed"


TYPE_STATUS_TASK = Literal[
    StatusTaskType.IN_QUEUE,
    StatusTaskType.IN_PROGRESS,
    StatusTaskType.COMPLETED,
    StatusTaskType.PAUSED,
    StatusTaskType.RETRY,
    StatusTaskType.FAILED
]
