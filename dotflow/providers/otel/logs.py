"""Opentelemetry"""

import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    LogExportResult
)
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from dotflow.providers.otel import (
    _setup_service,
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_PYTHON_LOG_LEVEL,
    OTEL_PYTHON_LOGGING_SCHEDULE_DELAY_MILLIS,
    OTEL_PYTHON_LOG_FORMAT
)


class _ConsoleLogExporter(ConsoleLogExporter):

    def export(self, *_args, **kwargs):
        return LogExportResult.SUCCESS


def _otlp_exporter(endpoint: str, insecure: bool):
    return OTLPLogExporter(
        endpoint=endpoint,
        insecure=insecure
    )


def _console_exporter():
    return _ConsoleLogExporter()


def setup_opentelemetry_logs_handler(
    service_name: str,
    endpoint: str,
    insecure: bool,
    level: int,
    schedule_delay_millis: int,
    format: str = "%(asctime)s - %(levelname)s [%(name)s]: %(message)s"
):
    provider = LoggerProvider(
        resource=_setup_service(
            service_name=service_name
        )
    )

    if endpoint:
        exporter = _otlp_exporter(endpoint=endpoint, insecure=insecure)
    else:
        exporter = _console_exporter()

    processor = BatchLogRecordProcessor(
        exporter=exporter,
        schedule_delay_millis=schedule_delay_millis
    )

    provider.add_log_record_processor(processor)

    set_logger_provider(provider)

    handler = LoggingHandler(
        level=level,
        logger_provider=provider
    )

    logging.basicConfig(
        format=format,
        level=logging.INFO,
    )

    logger = logging.getLogger(__name__)

    logger.addHandler(handler)
    logger.setLevel(level=level)

    return logger


client = setup_opentelemetry_logs_handler(
    service_name=OTEL_SERVICE_NAME,
    endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
    insecure=OTEL_EXPORTER_OTLP_INSECURE,
    level=OTEL_PYTHON_LOG_LEVEL,
    schedule_delay_millis=OTEL_PYTHON_LOGGING_SCHEDULE_DELAY_MILLIS,
    format=OTEL_PYTHON_LOG_FORMAT
)
