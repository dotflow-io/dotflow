"""Opentelemetry __init__ module."""

# flake8: noqa
# pylint: disable-all

import logging

from os import getenv

from dotenv import load_dotenv
from opentelemetry.sdk.resources import SERVICE_NAME, Resource, Attributes

from dotflow.utils import _type

load_dotenv()

OTEL_SERVICE_NAME = getenv("OTEL_SERVICE_NAME", "dotflow")
OTEL_EXPORTER_OTLP_ENDPOINT = _type(getenv("OTEL_EXPORTER_OTLP_ENDPOINT", None))
OTEL_EXPORTER_OTLP_INSECURE = _type(getenv("OTEL_EXPORTER_OTLP_INSECURE", True))
OTEL_METRICS_EXPORT_INTERVAL_MILLIS = _type(getenv("OTEL_METRICS_EXPORT_INTERVAL_MILLIS", 5000))

OTEL_PYTHON_LOG_CORRELATION = _type(getenv("OTEL_PYTHON_LOG_CORRELATION", "true"))
OTEL_PYTHON_LOG_FORMAT = getenv(
    "OTEL_PYTHON_LOG_FORMAT",
    "%(asctime)s - %(levelname)s [%(name)s]: %(message)s"
)
OTEL_PYTHON_LOG_LEVEL = _type(getenv("OTEL_PYTHON_LOG_LEVEL", logging.INFO))
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED = _type(getenv("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", True))
OTEL_PYTHON_LOGGING_SCHEDULE_DELAY_MILLIS = _type(getenv("OTEL_PYTHON_LOGGING_SCHEDULE_DELAY_MILLIS", 5000))
OTEL_PYTHON_EXCLUDED_URLS = getenv("OTEL_PYTHON_EXCLUDED_URLS", "client/.*/info,healthcheck")
OTEL_PYTHON_URLLIB3_EXCLUDED_URLS = getenv("OTEL_PYTHON_URLLIB3_EXCLUDED_URLS", "client/.*/info")
OTEL_PYTHON_REQUESTS_EXCLUDED_URLS = getenv("OTEL_PYTHON_REQUESTS_EXCLUDED_URLS", "healthcheck")


def _setup_service(service_name: str, attributes: Attributes = None) -> Resource:
    return Resource(
        attributes={
            SERVICE_NAME: service_name,
            **(attributes or {})
        }
    )
