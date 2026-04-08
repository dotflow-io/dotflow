from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from dotflow import Config, DotFlow, action
from dotflow.providers import TracerOpenTelemetry


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
    tracer = TracerOpenTelemetry(service_name="my-pipeline")

    provider = trace.get_tracer_provider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

    config = Config(tracer=tracer)

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.task.add(step=load)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
