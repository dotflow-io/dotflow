# Metrics OpenTelemetry

`MetricsOpenTelemetry` exports counters and histograms for workflow and task execution using the OpenTelemetry Metrics SDK. Use it to monitor throughput, duration, retries, and failures in Prometheus, Grafana, Datadog, or any OTLP-compatible backend.

/// note
Requires `pip install dotflow[otel]`
///

## Setup

```bash
pip install dotflow[otel]
```

## Basic example

Metrics are recorded internally by the SDK — no exporter needed for the provider to work.

{* ./docs_src/config/metrics_opentelemetry_basic.py hl[2,21:23] *}

## Exporting metrics

To visualize metrics, add an exporter. The example below prints metrics to the console.

```bash
pip install opentelemetry-exporter-otlp-proto-grpc
```

{* ./docs_src/config/metrics_opentelemetry.py hl[3:6,31:33] *}

## Exported metrics

| Metric | Type | When |
|--------|------|------|
| `dotflow_workflow_total` | Counter | Workflow starts, completes, or fails |
| `dotflow_workflow_duration_seconds` | Histogram | Workflow completes or fails |
| `dotflow_task_total` | Counter | Task completes or fails |
| `dotflow_task_duration_seconds` | Histogram | Task completes or fails |
| `dotflow_task_retry_total` | Counter | Task is retried |

## Lifecycle

| ABC method | When | Metric action |
|------------|------|---------------|
| `workflow_started` | Manager.__init__ | Increments `workflow_total{status=started}` |
| `workflow_completed` | _callback_workflow (success) | Increments `workflow_total{status=completed}`, records duration |
| `workflow_failed` | _callback_workflow (failure) | Increments `workflow_total{status=failed}`, records duration |
| `task_completed` | Task status = Completed | Increments `task_total{status=completed}`, records duration |
| `task_failed` | Task status = Failed | Increments `task_total{status=failed}`, records duration |
| `task_retried` | Task status = Retry | Increments `task_retry_total` |

## Compatible backends

| Backend | Exporter package |
|---------|-----------------|
| Prometheus | `opentelemetry-exporter-prometheus` |
| Grafana | `opentelemetry-exporter-otlp-proto-grpc` |
| Datadog | `opentelemetry-exporter-otlp-proto-grpc` |
| Console (debug) | Built-in (`ConsoleMetricExporter`) |

## References

- [MetricsOpenTelemetry](https://dotflow-io.github.io/dotflow/nav/reference/metrics-opentelemetry/)
- [MetricsDefault](https://dotflow-io.github.io/dotflow/nav/reference/metrics-default/)
