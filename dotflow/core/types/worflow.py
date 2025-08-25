"""Workflow Status Type module"""

from typing import Literal

from dotflow.core.types.enum import StrEnum


class WorkflowStatusType(StrEnum):
    """
    Import:
        You can import the **WorkflowStatusType** class with:

            from dotflow.core.types import WorkflowStatusType
    """

    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


WORKFLOW_STATUS_TYPE = Literal[
    WorkflowStatusType.IN_PROGRESS,
    WorkflowStatusType.COMPLETED
]
