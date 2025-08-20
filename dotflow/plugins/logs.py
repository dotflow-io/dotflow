"""Logs Handler"""

from dotflow.abc.logs import (
    Logs,
    TYPE_LOG,
    TASK_LOG_FORMAT
)
from dotflow.logging import logger


class LogsHandler(Logs):
    """Logs
    """

    def on_task_status_change(self, task_object, type: TYPE_LOG) -> None:
        new_log = getattr(logger, type.lower())
        new_log(
            TASK_LOG_FORMAT.format(
                task_id=task_object.task_id,
                workflow_id=task_object.workflow_id,
                status=task_object.status,
            )
        )
