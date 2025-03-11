"""Type TaskStatus mode module"""

from typing_extensions import Annotated, Doc


class TaskStatus:
    """
    Import:
        You can import the **TaskStatus** class with:

            from dotflow.core.types import TaskStatus
    """

    NOT_STARTED: Annotated[str, Doc("Status not started.")] = "Not started"
    IN_PROGRESS: Annotated[str, Doc("Status in progress.")] = "In progress"
    COMPLETED: Annotated[str, Doc("Status completed.")] = "Completed"
    PAUSED: Annotated[str, Doc("Status paused.")] = "Paused"
    RETRY: Annotated[str, Doc("Status retry.")] = "Retry"
    FAILED: Annotated[str, Doc("Status failed.")] = "Failed"
