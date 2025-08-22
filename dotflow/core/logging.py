"""Opentelemetry"""

import os

import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


def setup_opentelemetry_handler(
    service_name: str,
    endpoint: str,
    insecure: bool,
    level: int
):
    resource = Resource({SERVICE_NAME: service_name})
    provider = LoggerProvider(resource=resource)

    processor = BatchLogRecordProcessor(
        OTLPLogExporter(
            endpoint=endpoint,
            insecure=insecure
        )
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

    logger = logging.getLogger(__name__)

    logger.addHandler(handler)
    logger.setLevel(level=level)
    logger.addHandler(logging.StreamHandler())

    return logger


logger = setup_opentelemetry_handler(
    service_name=os.getenv("OTEL_SERVICE_NAME", "dotflow"),
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "0.0.0.0:4317"),
    insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", True),
    level=os.getenv("OTEL_LEVEL", logging.INFO)
)
