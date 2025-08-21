"""Logs ABC"""

from typing import Literal

from abc import ABC, abstractmethod

from dotflow.core.types.enum import StrEnum


class TypeLog(StrEnum):

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


TYPE_LOG = Literal[
    TypeLog.CRITICAL,
    TypeLog.ERROR,
    TypeLog.WARNING,
    TypeLog.INFO,
    TypeLog.DEBUG,
    TypeLog.NOTSET,
]

TASK_LOG_FORMAT = "{task_id}: {workflow_id} - {status}"
WORKFLOW_LOG_FORMAT = "{workflow_id}: {status}"


class Logs(ABC):
    """Logs"""

    group = "logs"

    @abstractmethod
    def on_task_status_change(self, task_object, type: TYPE_LOG) -> None:
        pass
