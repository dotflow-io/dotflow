"""Logs Default"""

from dotflow.abc.logs import (
    Logs,
    TYPE_LOG,
    TASK_LOG_FORMAT,
    WORKFLOW_LOG_FORMAT
)
from dotflow.logging import logger


class LogsHandler(Logs):

    def post_task(
        self,
        task_id: int,
        wotkflow_id: str,
        status: str,
        type: TYPE_LOG
    ) -> None:
        new_log = getattr(logger, type.lower())
        new_log(
            TASK_LOG_FORMAT.format(
                task_id=task_id,
                workflow_id=wotkflow_id,
                status=status,
            )
        )

    def post_workflow(
        self,
        wotkflow_id: str,
        status: str,
        type: TYPE_LOG
    ) -> None:
        new_log = getattr(logger, type.lower())
        new_log(
            WORKFLOW_LOG_FORMAT.format(
                workflow_id=wotkflow_id,
                status=status,
            )
        )
