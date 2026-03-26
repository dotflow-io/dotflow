"""Type TypeStatus mode module"""

from typing import Annotated

from typing_extensions import Doc


class TypeStatus:
    """
    Import:
        You can import the **TypeStatus** class with:

            from dotflow.core.types import TypeStatus
    """

    NOT_STARTED: Annotated[str, Doc("Status not started.")] = "Not started"
    IN_PROGRESS: Annotated[str, Doc("Status in progress.")] = "In progress"
    COMPLETED: Annotated[str, Doc("Status completed.")] = "Completed"
    PAUSED: Annotated[str, Doc("Status paused.")] = "Paused"
    RETRY: Annotated[str, Doc("Status retry.")] = "Retry"
    FAILED: Annotated[str, Doc("Status failed.")] = "Failed"

    @classmethod
    def get_symbol(cls, value: str) -> str:
        status = {
            TypeStatus.NOT_STARTED: "⚪",
            TypeStatus.IN_PROGRESS: "🔵",
            TypeStatus.COMPLETED: "✅",
            TypeStatus.PAUSED: "◼️",
            TypeStatus.RETRY: "❗",
            TypeStatus.FAILED: "❌",
        }
        return status.get(value)
