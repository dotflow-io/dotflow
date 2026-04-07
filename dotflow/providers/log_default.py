"""Log Default"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from dotflow.abc.log import Log
from dotflow.settings import Settings as settings

LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class LogDefault(Log):
    """
    Import:
        You can import the **LogDefault** class with:

            from dotflow.providers import LogDefault

    Args:
        level (str): Minimum log level. One of DEBUG, INFO, WARNING, ERROR.
            Defaults to INFO.

        output (str): Log destination. One of file, console, both.
            Defaults to file.

        path (str): Path to the log file. Only used when output is file or both.
            Defaults to .output/flow.log.

        format (str): Message format. One of simple, json.
            Defaults to simple.
    """

    def __init__(
        self,
        level: str = "INFO",
        output: str = "console",
        path: str = str(settings.LOG_PATH),
        format: str = "simple",
    ) -> None:
        self._level = LEVELS.get(level.upper(), logging.INFO)
        self._output = output
        self._format = format
        self._logger = self._setup_logger(path)

    def info(self, **kwargs) -> None:
        self._log(logging.INFO, **kwargs)

    def error(self, **kwargs) -> None:
        self._log(logging.ERROR, **kwargs)

    def warning(self, **kwargs) -> None:
        self._log(logging.WARNING, **kwargs)

    def debug(self, **kwargs) -> None:
        self._log(logging.DEBUG, **kwargs)

    def _log(self, level: int, **kwargs) -> None:
        if level < self._level:
            return

        task = kwargs.get("task")
        if task:
            message = self._format_task(level, task)
        else:
            message = self._format_kwargs(kwargs)

        self._logger.log(level, message)

    def _format_task(self, level: int, task) -> str:
        if self._format == "json":
            data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": logging.getLevelName(level),
                "workflow_id": str(task.workflow_id),
                "task_id": str(task.task_id),
                "status": str(task.status),
            }
            if task.duration:
                data["duration"] = task.duration
            if task.retry_count:
                data["retry_count"] = task.retry_count
            if task.errors and level >= logging.ERROR:
                last_error = task.errors[-1]
                data["error"] = {
                    "exception": str(last_error.exception),
                    "message": str(last_error.message),
                }
            return json.dumps(data)

        message = f"ID {task.workflow_id} - {task.task_id} - {task.status}"
        if task.errors and level >= logging.ERROR:
            message += f" \n {task.errors[-1].traceback}"

        return message

    def _format_kwargs(self, kwargs: dict) -> str:
        if self._format == "json":
            return json.dumps({k: str(v) for k, v in kwargs.items()})
        return str(kwargs)

    def _setup_logger(self, path: str) -> logging.Logger:
        logger = logging.getLogger(f"dotflow.{id(self)}")
        logger.setLevel(self._level)
        logger.handlers.clear()
        logger.propagate = False

        fmt = logging.Formatter(settings.LOG_FORMAT)

        if self._output in ("file", "both"):
            filepath = Path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(filepath, mode="a")
            fh.setLevel(self._level)
            fh.setFormatter(fmt)
            logger.addHandler(fh)

        if self._output in ("console", "both"):
            ch = logging.StreamHandler()
            ch.setLevel(self._level)
            ch.setFormatter(fmt)
            logger.addHandler(ch)

        return logger
