"""Notify Default"""

from typing import Any

from dotflow.abc.log import Log
from dotflow.logging import logger


class LogDefault(Log):
    def info(self, task: Any) -> None:
        logger.info(
            "ID %s - %s - %s",
            task.workflow_id,
            task.task_id,
            task.status,
        )

    def error(self, task: Any) -> None:
        logger.error(
            "ID %s - %s - %s \n %s",
            task.workflow_id,
            task.task_id,
            task.status,
            task.errors[-1].traceback if task.errors else "",
        )
