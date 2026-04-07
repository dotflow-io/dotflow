from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from dotflow import Config, DotFlow, action
from dotflow.providers import LogOpenTelemetry


@action
def extract():
    return {"data": "fetched"}


@action
def transform(previous_context):
    return {"result": previous_context.storage}


def main():
    resource = Resource.create({"service.name": "my-pipeline"})
    provider = LoggerProvider(resource=resource)
    provider.add_log_record_processor(
        SimpleLogRecordProcessor(OTLPLogExporter())
    )
    set_logger_provider(provider)

    config = Config(
        log=LogOpenTelemetry(service_name="my-pipeline"),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
