"""Log OpenTelemetry"""

from __future__ import annotations

import logging
from pathlib import Path

from dotflow.abc.log import LEVELS, Log
from dotflow.core.exception import ModuleNotFound
from dotflow.settings import Settings as settings


class LogOpenTelemetry(Log):
    """
    Import:
        You can import the **LogOpenTelemetry** class with:

            from dotflow.providers import LogOpenTelemetry

    Example:
        `class` dotflow.providers.log_opentelemetry.LogOpenTelemetry

            from dotflow import Config, DotFlow
            from dotflow.providers import LogOpenTelemetry

            config = Config(
                log=LogOpenTelemetry(service_name="my-pipeline"),
            )

            workflow = DotFlow(config=config)

    Args:
        service_name (str): The service name used in the OpenTelemetry logger.
        level (str): Minimum log level. One of DEBUG, INFO, WARNING, ERROR.
            Defaults to INFO.
        output (str): Log destination. One of console, file, both.
            Defaults to console.
        path (str): Path to the log file. Only used when output is file or both.
            Defaults to .output/flow.log.
        format (str): Message format. One of simple, json.
            Defaults to simple.
    """

    def __init__(
        self,
        service_name: str = "dotflow",
        level: str = "INFO",
        output: str = "console",
        path: str = str(settings.LOG_PATH),
        format: str = "simple",
    ) -> None:
        try:
            from opentelemetry._logs import set_logger_provider
            from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
            from opentelemetry.sdk._logs.export import (
                ConsoleLogExporter,
                SimpleLogRecordProcessor,
            )
            from opentelemetry.sdk.resources import Resource
        except ImportError as err:
            raise ModuleNotFound(
                module="opentelemetry", library="dotflow[otel]"
            ) from err

        self._level = LEVELS.get(level.upper(), logging.INFO)
        self._format = format

        resource = Resource.create({"service.name": service_name})
        provider = LoggerProvider(resource=resource)
        set_logger_provider(provider)

        if output in ("console", "both"):
            provider.add_log_record_processor(
                SimpleLogRecordProcessor(ConsoleLogExporter())
            )

        handler = LoggingHandler(level=self._level, logger_provider=provider)

        self._logger = logging.getLogger(f"dotflow.otel.{id(self)}")
        self._logger.setLevel(self._level)
        self._logger.handlers.clear()
        self._logger.propagate = False
        self._logger.addHandler(handler)

        if output in ("file", "both"):
            filepath = Path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(filepath, mode="a")
            fh.setLevel(self._level)
            fh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
            self._logger.addHandler(fh)
