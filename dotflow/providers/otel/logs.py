"""Opentelemetry"""

import os

import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from dotflow.providers.otel import (
    setup_service,
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_LOGS_LEVEL,
    OTEL_LOGS_SCHEDULE_DELAY_MILLIS
)


def setup_opentelemetry_logs_handler(
    service_name: str,
    endpoint: str,
    insecure: bool,
    level: int,
    schedule_delay_millis: int
):
    exporter = OTLPLogExporter(
        endpoint=endpoint,
        insecure=insecure
    )

    provider = LoggerProvider(
        resource=setup_service(service_name=service_name)
    )

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
        format="%(asctime)s - %(levelname)s [%(name)s]: %(message)s",
        level=logging.INFO,
    )

    client = logging.getLogger(__name__)

    client.addHandler(handler)
    client.setLevel(level=level)

    return client


client = setup_opentelemetry_logs_handler(
    service_name=os.getenv("OTEL_SERVICE_NAME", OTEL_SERVICE_NAME),
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", OTEL_EXPORTER_OTLP_ENDPOINT),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", OTEL_EXPORTER_OTLP_INSECURE),
    level=os.getenv("OTEL_LOGS_LEVEL", OTEL_LOGS_LEVEL),
    schedule_delay_millis=os.getenv("OTEL_LOGS_SCHEDULE_DELAY_MILLIS", OTEL_LOGS_SCHEDULE_DELAY_MILLIS)
)
