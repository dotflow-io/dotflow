# Providers

**Providers** are pluggable backends wired through [`Config`](../reference/config.md). They let the same workflow code use different storage, notifications, logging, tracing, metrics, and scheduling without changing task logic.

## Families

| Provider | Purpose | Built-in | Integrations |
|----------|---------|----------|--------------|
| **Storage** | Persists task context and checkpoints | Default (memory), File | S3, GCS |
| **Notify** | Sends alerts on status changes | Default (no-op) | Telegram, Discord |
| **Log** | Structured logging for runs | Default (console/file) | OpenTelemetry, Sentry |
| **Tracer** | Distributed traces per workflow/task | Default (no-op) | OpenTelemetry, Sentry |
| **Metrics** | Counters and histograms | Default (no-op) | OpenTelemetry |
| **Scheduler** | Drives recurring execution | Default (no-op) | Cron |
| **Server** | Sends execution data to remote API | ServerDefault (auto-detected) | — |

You pass instances into `Config`:

```python
from dotflow import Config
from dotflow.providers import StorageFile, LogDefault, TracerOpenTelemetry

config = Config(
    storage=StorageFile(path=".output"),
    log=LogDefault(output="console", format="json"),
    tracer=TracerOpenTelemetry(service_name="my-pipeline"),
)
```

Built-in providers use **core** dependencies. Cloud and observability integrations need **pip extras**:

| Extra | Install | Providers |
|-------|---------|-----------|
| `dotflow[scheduler]` | croniter | SchedulerCron |
| `dotflow[aws]` | boto3 | StorageS3 |
| `dotflow[gcp]` | google-cloud-storage | StorageGCS |
| `dotflow[otel]` | opentelemetry-api, opentelemetry-sdk | LogOpenTelemetry, TracerOpenTelemetry, MetricsOpenTelemetry |
| `dotflow[sentry]` | sentry-sdk | LogSentry, TracerSentry |

## Why it matters

- **Durability**: storage + [checkpoints](../tutorial/checkpoint.md) enable resume after failure.
- **Observability**: log, tracer, and metrics providers surface failures, retries, and performance.
- **Notifications**: notify providers alert teams via Telegram, Discord, or custom webhooks.
- **Operations**: swap file storage in development for S3 or GCS in production with one config change.

## References

- [`Config`](../reference/config.md)
- [Custom providers](../development/custom-providers.md)
- [Integrations](../integrations/index.md)
- Abstract bases: [`Storage`](../reference/abc-storage.md), [`Notify`](../reference/abc-notify.md), [`Log`](../reference/abc-log.md), [`Scheduler`](../reference/abc-scheduler.md), [`Tracer`](../reference/abc-tracer.md), [`Metrics`](../reference/abc-metrics.md), [`Server`](../reference/abc-server.md)
