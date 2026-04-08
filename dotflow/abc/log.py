"""Log ABC"""

from __future__ import annotations

import logging
from abc import ABC
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class LogRecordError(BaseModel):
    exception: str = Field(default="")
    message: str = Field(default="")


class LogRecord(BaseModel):
    timestamp: str = Field(default="")
    level: str = Field(default="")
    workflow_id: str = Field(default="")
    task_id: str = Field(default="")
    status: str = Field(default="")
    duration: Optional[float] = Field(default=None)
    retry_count: Optional[int] = Field(default=None)
    error: Optional[LogRecordError] = Field(default=None)


class Log(ABC):
    """Log

    Base class for all log providers. Subclasses must set
    ``self._logger``, ``self._level`` and ``self._format``
    in their ``__init__``.
    """

    _logger: logging.Logger
    _level: int = logging.INFO
    _format: str = "simple"

    def info(self, **kwargs) -> None:
        """Info"""
        self._log(logging.INFO, **kwargs)

    def error(self, **kwargs) -> None:
        """Error"""
        self._log(logging.ERROR, **kwargs)

    def warning(self, **kwargs) -> None:
        """Warning"""
        self._log(logging.WARNING, **kwargs)

    def debug(self, **kwargs) -> None:
        """Debug"""
        self._log(logging.DEBUG, **kwargs)

    _FORMATTERS = {
        "json": "_format_json",
        "simple": "_format_text",
    }

    def _log(self, level: int, **kwargs) -> None:
        if level < self._level:
            return

        formatter = getattr(
            self, self._FORMATTERS.get(self._format, "_format_text")
        )
        task = kwargs.get("task")

        if task:
            message = formatter(level, task=task)
        else:
            message = formatter(level, **kwargs)

        self._logger.log(level, message)

    def _format_json(self, level: int, **kwargs) -> str:
        task = kwargs.get("task")
        if task:
            record = LogRecord(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=logging.getLevelName(level),
                workflow_id=str(task.workflow_id),
                task_id=str(task.task_id),
                status=str(task.status),
            )

            if task.duration is not None:
                record.duration = task.duration

            if task.retry_count:
                record.retry_count = task.retry_count

            if task.errors and level >= logging.ERROR:
                last_error = task.errors[-1]
                record.error = LogRecordError(
                    exception=str(last_error.exception),
                    message=str(last_error.message),
                )

            return record.model_dump_json(exclude_none=True)

        record = LogRecord(**{k: str(v) for k, v in kwargs.items()})
        return record.model_dump_json(exclude_none=True)

    def _format_text(self, level: int, **kwargs) -> str:
        task = kwargs.get("task")
        if task:
            message = f"ID {task.workflow_id} - {task.task_id} - {task.status}"
            if task.errors and level >= logging.ERROR:
                message += f" \n {task.errors[-1].traceback}"
            return message

        return str(kwargs)
