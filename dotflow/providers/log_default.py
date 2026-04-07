"""Log Default"""

from __future__ import annotations

import logging
from pathlib import Path

from dotflow.abc.log import LEVELS, Log
from dotflow.settings import Settings as settings


class LogDefault(Log):
    """
    Import:
        You can import the **LogDefault** class with:

            from dotflow.providers import LogDefault

    Args:
        level (str): Minimum log level. One of DEBUG, INFO, WARNING, ERROR.
            Defaults to INFO.

        output (str): Log destination. One of file, console, both.
            Defaults to console.

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
        self._format = format

        self._logger = logging.getLogger(f"dotflow.{id(self)}")
        self._logger.setLevel(self._level)
        self._logger.handlers.clear()
        self._logger.propagate = False

        fmt = logging.Formatter(settings.LOG_FORMAT)

        if output in ("file", "both"):
            filepath = Path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(filepath, mode="a")
            fh.setLevel(self._level)
            fh.setFormatter(fmt)
            self._logger.addHandler(fh)

        if output in ("console", "both"):
            ch = logging.StreamHandler()
            ch.setLevel(self._level)
            ch.setFormatter(fmt)
            self._logger.addHandler(ch)
