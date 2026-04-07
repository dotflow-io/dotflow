# Log OpenTelemetry

`LogOpenTelemetry` emits structured log records using the OpenTelemetry Logs SDK. Logs are exported to any OTLP-compatible backend or printed to the console.

Use this when you want your dotflow logs to appear alongside traces and metrics in the same observability platform.

/// note
Requires `pip install dotflow[otel]`
///

## Setup

```bash
pip install dotflow[otel]
```

## Basic example

Pass `console=True` to emit log records to the console — useful for local development.

{* ./docs_src/config/log_opentelemetry_basic.py hl[2,16:18] *}

## Exporting logs

To send logs to an OTLP-compatible backend (Loki, Datadog, Elastic, etc.), configure a provider with the OTLP exporter before creating the `LogOpenTelemetry` instance.

```bash
pip install opentelemetry-exporter-otlp-proto-grpc
```

{* ./docs_src/config/log_opentelemetry.py hl[2,24:27] *}

## Log levels

| Level | Logged when |
|-------|-------------|
| `INFO` | Task status changes (Not started, In progress, Completed) |
| `WARNING` | Task status changes to Retry |
| `ERROR` | Task status changes to Failed (includes traceback) |
| `DEBUG` | Available for custom use |

## How it differs from LogDefault

| Feature | LogDefault | LogOpenTelemetry |
|---------|-----------|-----------------|
| Output | File / Console | OTel Logs SDK |
| Format | Simple text or JSON | OTel LogRecord |
| Backend | Local file | Loki, Datadog, Elastic, any OTLP |
| Correlation | None | Shares service.name with Tracer/Metrics |

## Full observability stack

Use all three OpenTelemetry providers together:

```python
from dotflow import Config, DotFlow
from dotflow.providers import LogOpenTelemetry, TracerOpenTelemetry, MetricsOpenTelemetry

config = Config(
    log=LogOpenTelemetry(service_name="my-pipeline"),
    tracer=TracerOpenTelemetry(service_name="my-pipeline"),
    metrics=MetricsOpenTelemetry(service_name="my-pipeline"),
)

workflow = DotFlow(config=config)
```

## References

- [LogOpenTelemetry](https://dotflow-io.github.io/dotflow/nav/reference/log-opentelemetry/)
- [Log Default](https://dotflow-io.github.io/dotflow/nav/tutorial/log-default/)
- [Tracer OpenTelemetry](https://dotflow-io.github.io/dotflow/nav/tutorial/tracer-opentelemetry/)
- [Metrics OpenTelemetry](https://dotflow-io.github.io/dotflow/nav/tutorial/metrics-opentelemetry/)
