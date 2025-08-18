"""Workflow Status Type module"""

from enum import StrEnum
from typing import Literal


class WorkflowStatusType(StrEnum):
    """
    Import:
        You can import the **WorkflowStatusType** class with:

            from dotflow.core.types import WorkflowStatusType
    """

    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


WORKFLOW_STATUS_TYPE = Literal[
    WorkflowStatusType.NEW,
    WorkflowStatusType.IN_PROGRESS,
    WorkflowStatusType.COMPLETED
]