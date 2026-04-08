# Tracer OpenTelemetry

`TracerOpenTelemetry` exports distributed traces for every workflow and task execution using the OpenTelemetry standard. Each workflow becomes a parent span, each task becomes a child span with duration, status, retry events, and error details.

/// note
Requires `pip install dotflow[otel]`
///

## Setup

```bash
pip install dotflow[otel]
```

## Basic example

Traces are created internally by the SDK — no exporter is needed for the provider to work.

{* ./docs_src/config/tracer_opentelemetry_basic.py hl[2,21:23] *}

## Exporting traces

To visualize traces, add an exporter. The example below sends traces to the console and to any OTLP-compatible backend (Jaeger, Tempo, Datadog, etc.).

```bash
pip install opentelemetry-exporter-otlp-proto-grpc
```

{* ./docs_src/config/tracer_opentelemetry.py hl[2:3,28:29] *}

## Running Jaeger locally

```bash
docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
```

Run the example and open [http://localhost:16686](http://localhost:16686) to see traces.

## Trace structure

```
[Trace: workflow_id=550e8400...]
  └── [Span: task:0] 0.5s OK — Completed
  └── [Span: task:1] 1.2s OK — Completed
  └── [Span: task:2] 0.3s ERROR — Failed
        └── [Event: exception — ValueError "connection refused"]
```

## Span attributes

| Attribute | Source |
|-----------|--------|
| `dotflow.workflow_id` | `task.workflow_id` |
| `dotflow.task_id` | `task.task_id` |
| `dotflow.task.status` | `task.status` |
| `dotflow.task.duration` | `task.duration` |
| `dotflow.task.retry_count` | `task.retry_count` |

## Lifecycle

| ABC method | When | Span action |
|------------|------|-------------|
| `start_workflow` | Manager.__init__ | Creates parent span |
| `start_task` | TaskEngine.start() | Creates child span |
| `end_task` | TaskEngine.start() finally | Sets attributes, status, ends span |
| `end_workflow` | _callback_workflow | Sets workflow status, ends parent span |

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

- [TracerOpenTelemetry](https://dotflow-io.github.io/dotflow/nav/reference/tracer-opentelemetry/)
- [TracerDefault](https://dotflow-io.github.io/dotflow/nav/reference/tracer-default/)
