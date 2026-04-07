"""Log Default"""

from dotflow.abc.log import Log
from dotflow.logging import logger


class LogDefault(Log):
    def info(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            logger.info(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            logger.info("%s", kwargs)

    def error(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            logger.error(
                "ID %s - %s - %s \n %s",
                task.workflow_id,
                task.task_id,
                task.status,
                task.errors[-1].traceback if task.errors else "",
            )
        else:
            logger.error("%s", kwargs)

    def warning(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            logger.warning(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            logger.warning("%s", kwargs)

    def debug(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            logger.debug(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            logger.debug("%s", kwargs)
