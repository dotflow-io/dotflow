"""Opentelemetry __init__ module."""

import logging

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

OTEL_SERVICE_NAME = "dotflow"
OTEL_EXPORTER_OTLP_ENDPOINT = "0.0.0.0:4317"
OTEL_EXPORTER_OTLP_INSECURE = True
OTEL_LOGS_LEVEL = logging.INFO
OTEL_LOGS_SCHEDULE_DELAY_MILLIS = 5000
OTEL_METRICS_EXPORT_INTERVAL_MILLIS = 5000


def setup_service(service_name: str):
    return Resource({SERVICE_NAME: service_name})
