"""Log OpenTelemetry"""

from __future__ import annotations

import logging

from dotflow.abc.log import Log
from dotflow.core.exception import ModuleNotFound


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
    """

    def __init__(self, service_name: str = "dotflow") -> None:
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

        resource = Resource.create({"service.name": service_name})
        provider = LoggerProvider(resource=resource)
        set_logger_provider(provider)

        provider.add_log_record_processor(
            SimpleLogRecordProcessor(ConsoleLogExporter())
        )

        handler = LoggingHandler(level=logging.DEBUG, logger_provider=provider)

        self._logger = logging.getLogger(f"dotflow.otel.{id(self)}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()
        self._logger.propagate = False
        self._logger.addHandler(handler)

    def info(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.info(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            self._logger.info("%s", kwargs)

    def error(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.error(
                "ID %s - %s - %s \n %s",
                task.workflow_id,
                task.task_id,
                task.status,
                task.errors[-1].traceback if task.errors else "",
            )
        else:
            self._logger.error("%s", kwargs)

    def warning(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.warning(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            self._logger.warning("%s", kwargs)

    def debug(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.debug(
                "ID %s - %s - %s",
                task.workflow_id,
                task.task_id,
                task.status,
            )
        else:
            self._logger.debug("%s", kwargs)
