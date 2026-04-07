# Log Default

`LogDefault` is the built-in log provider. It supports file logging, console logging, or both, with simple text or JSON output format.

This is the provider used when no log is explicitly configured in `Config`.

## Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` | Minimum log level |
| `output` | `file`, `console`, `both` | `console` | Where logs are written |
| `path` | Any file path | `.output/flow.log` | Log file location (used with `file` or `both`) |
| `format` | `simple`, `json` | `simple` | Message format |

## Basic example

Console output with simple format:

{* ./docs_src/config/log_default.py hl[2,16:19] *}

Output:

```
2026-04-07 14:31:07 - INFO [dotflow]: ID abc-123 - 0 - Not started
2026-04-07 14:31:07 - INFO [dotflow]: ID abc-123 - 0 - In progress
2026-04-07 14:31:07 - INFO [dotflow]: ID abc-123 - 0 - Completed
```

## JSON format

JSON output to both console and file — useful for log aggregation tools (ELK, Loki, Datadog).

{* ./docs_src/config/log_default_json.py hl[2,16:21] *}

Output:

```json
{"timestamp": "2026-04-07T19:34:24.626Z", "level": "INFO", "workflow_id": "abc-123", "task_id": "0", "status": "Completed", "duration": 0.0001}
```

## Log levels

| Level | Logged when |
|-------|-------------|
| `INFO` | Task status changes (Not started, In progress, Completed) |
| `WARNING` | Task status changes to Retry |
| `ERROR` | Task status changes to Failed (includes traceback) |
| `DEBUG` | Available for custom use |

## References

- [LogDefault](https://dotflow-io.github.io/dotflow/nav/reference/log-default/)
- [Log OpenTelemetry](https://dotflow-io.github.io/dotflow/nav/tutorial/log-opentelemetry/)
