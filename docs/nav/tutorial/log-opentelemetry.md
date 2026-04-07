# Log OpenTelemetry

`LogOpenTelemetry` exports traces and spans for every workflow and task execution using the OpenTelemetry standard. Each workflow becomes a trace, each task becomes a child span with duration, status, retry count, and error events.

One provider, all backends — Jaeger, Grafana Tempo, Datadog, Honeycomb, New Relic, AWS X-Ray, Google Cloud Trace.

/// note
Requires `pip install dotflow[otel]`
///

## Setup

```bash
pip install dotflow[otel]
```

## Basic example

Use `LogOpenTelemetry` as the log provider in `Config`. Traces are created internally by the SDK — no exporter is needed for the provider to work.

{* ./docs_src/config/log_opentelemetry.py hl[2,21:23] *}

## Exporting traces

To visualize traces, add an exporter. The example below sends traces to the console and to any OTLP-compatible backend (Jaeger, Tempo, Datadog, etc.).

```bash
pip install opentelemetry-exporter-otlp-proto-grpc
```

{* ./docs_src/config/log_opentelemetry_export.py hl[2:3,28:29] *}

## Running Jaeger locally

```bash
docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
```

Run the export example and open [http://localhost:16686](http://localhost:16686) — select the service name to see traces.

## Trace structure

Each workflow creates a parent span. Each task is a child span under it.

```
[Trace: workflow_id=550e8400...]
  └── [Span: task:0] 0.5s OK — Completed
  └── [Span: task:1] 1.2s OK — Completed
  └── [Span: task:2] 0.3s ERROR — Failed
        └── [Event: exception — ValueError "connection refused"]
        └── [Event: retry — attempt 1]
        └── [Event: retry — attempt 2]
```

## Span attributes

Every task span includes:

| Attribute | Source |
|-----------|--------|
| `dotflow.workflow_id` | `task.workflow_id` |
| `dotflow.task_id` | `task.task_id` |
| `dotflow.task.status` | `task.status` |
| `dotflow.task.duration` | `task.duration` |
| `dotflow.task.retry_count` | `task.retry_count` |

## How it maps to log levels

| Log level | When | Span action |
|-----------|------|-------------|
| `info` | Status changes to Completed | Sets span status OK, ends span |
| `error` | Status changes to Failed | Adds exception event, sets span status ERROR, ends span |
| `warning` | Status changes to Retry | Adds retry event with attempt count |
| `debug` | — | No-op |

## Compatible backends

| Backend | Exporter package |
|---------|-----------------|
| Jaeger | `opentelemetry-exporter-otlp-proto-grpc` |
| Grafana Tempo | `opentelemetry-exporter-otlp-proto-grpc` |
| Datadog | `opentelemetry-exporter-otlp-proto-grpc` |
| Honeycomb | `opentelemetry-exporter-otlp-proto-grpc` |
| New Relic | `opentelemetry-exporter-otlp-proto-grpc` |
| AWS X-Ray | `opentelemetry-exporter-otlp-proto-grpc` |
| Google Cloud Trace | `opentelemetry-exporter-gcp-trace` |
| Console (debug) | Built-in (`ConsoleSpanExporter`) |

## References

- [LogOpenTelemetry](https://dotflow-io.github.io/dotflow/nav/reference/log-opentelemetry/)
- [Log Default](https://dotflow-io.github.io/dotflow/nav/tutorial/log-default/)
- [OpenTelemetry Python docs](https://opentelemetry-python.readthedocs.io/)
