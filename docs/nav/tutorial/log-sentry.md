# Log Sentry

`LogSentry` sends task errors to [Sentry](https://sentry.io) for real-time error monitoring. Status changes are recorded as breadcrumbs for context.

Use this when your workflows run in production (Lambda, Cloud Run, servers) and you need error tracking beyond local logs.

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
| `dsn` | `str` | — | Sentry DSN for the project (required) |
| `environment` | `str \| None` | `None` | Environment tag sent to Sentry |
| `traces_sample_rate` | `float` | `0.0` | Sample rate for performance traces (0.0 to 1.0) |

## Basic example

{* ./docs_src/config/log_sentry.py hl[2,16:20] *}

## What gets captured

| Event | Sentry action |
|-------|---------------|
| Task status changes (info) | Breadcrumb |
| Task retries (warning) | Breadcrumb |
| Task failures (error) | `capture_message` with extras |
| Debug events | Ignored |

Each error capture includes:

- `workflow_id` — which workflow failed
- `task_id` — which task failed
- `exception` — exception type
- `attempt` — retry attempt number
- `traceback` — full traceback

## Combining with other log providers

Sentry is for error monitoring, not general logging. Use it alongside `LogDefault` or `LogOpenTelemetry` by choosing one per workflow:

```python
from dotflow import Config, DotFlow
from dotflow.providers import LogSentry

# Production: errors go to Sentry
prod_config = Config(
    log=LogSentry(dsn="https://xxx@sentry.io/123", environment="production"),
)

# Development: logs go to console
from dotflow.providers import LogDefault
dev_config = Config(
    log=LogDefault(output="console", format="json"),
)
```

## References

- [LogSentry](https://dotflow-io.github.io/dotflow/nav/reference/log-sentry/)
- [Log Default](https://dotflow-io.github.io/dotflow/nav/tutorial/log-default/)
- [Log OpenTelemetry](https://dotflow-io.github.io/dotflow/nav/tutorial/log-opentelemetry/)
