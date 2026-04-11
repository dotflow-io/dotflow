from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource

from dotflow import Config, DotFlow, action
from dotflow.providers import MetricsOpenTelemetry


@action
def extract():
    return {"data": "fetched"}


@action
def transform(previous_context):
    return {"result": previous_context.storage}


@action(retry=3)
def load(previous_context):
    return {"saved": previous_context.storage}


def main():
    m = MetricsOpenTelemetry(service_name="my-pipeline")

    reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    provider = metrics.get_meter_provider()
    provider._all_metric_readers.add(reader)

    config = Config(metrics=m)

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.task.add(step=load)
    workflow.start()

    reader.force_flush()
    return workflow


if __name__ == "__main__":
    main()
