"""Opentelemetry"""

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from dotflow.providers.otel import (
    _setup_service,
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_INSECURE,
    OTEL_METRICS_EXPORT_INTERVAL_MILLIS
)


def setup_opentelemetry_metrics_handler(
    service_name: str,
    endpoint: str,
    insecure: bool,
    export_interval_millis: int
):
    exporter = OTLPMetricExporter(
        endpoint=endpoint,
        insecure=insecure
    )

    reader = PeriodicExportingMetricReader(
        exporter=exporter,
        export_interval_millis=export_interval_millis
    )

    provider = MeterProvider(
        resource=_setup_service(service_name=service_name),
        metric_readers=[reader]
    )

    metrics.set_meter_provider(provider)

    meter = metrics.get_meter(__name__)

    return meter


client = setup_opentelemetry_metrics_handler(
    service_name=OTEL_SERVICE_NAME,
    endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
    insecure=OTEL_EXPORTER_OTLP_INSECURE,
    export_interval_millis=OTEL_METRICS_EXPORT_INTERVAL_MILLIS
)
