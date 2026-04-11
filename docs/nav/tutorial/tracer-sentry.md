# Tracer Sentry

`TracerSentry` uses [Sentry Performance Monitoring](https://docs.sentry.io/product/performance/) to create transactions per workflow and spans per task.

Use this when you want to track task durations, identify slow tasks, and see the full workflow waterfall in the Sentry dashboard.

/// note
Requires `pip install dotflow[sentry]`
///

## Setup

```bash
pip install dotflow[sentry]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dsn` | `str \| None` | `None` | Sentry DSN. If None, reuses the SDK already initialized (e.g. by LogSentry) |
| `environment` | `str \| None` | `None` | Environment tag sent to Sentry |
| `traces_sample_rate` | `float` | `1.0` | Sample rate for performance traces (0.0 to 1.0) |

## Basic example

{* ./docs_src/config/tracer_sentry.py hl[2,17:22] *}

## What gets captured

| Event | Sentry action |
|-------|---------------|
| Workflow starts | Transaction created (`op="workflow"`) |
| Workflow ends | Transaction finished with status `ok` or `internal_error` |
| Task starts | Child span created (`op="task"`) |
| Task ends | Span finished with duration, retry count, and error details |

## Full Sentry stack

Use both `LogSentry` and `TracerSentry` together for error tracking + performance monitoring:

{* ./docs_src/config/sentry_full.py hl[2,17:24] *}

/// tip
When using both providers, pass the `dsn` only to `LogSentry`. `TracerSentry` reuses the already initialized SDK — no need to pass `dsn` again.
///

## References

- [TracerSentry](https://dotflow-io.github.io/dotflow/nav/reference/tracer-sentry/)
- [LogSentry](https://dotflow-io.github.io/dotflow/nav/tutorial/log-sentry/)
- [Tracer OpenTelemetry](https://dotflow-io.github.io/dotflow/nav/tutorial/tracer-opentelemetry/)
