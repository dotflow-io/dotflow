# Providers

**Providers** are pluggable backends wired through [`Config`](../reference/config.md). They let the same workflow code use different storage, notifications, logging, and scheduling without changing task logic.

## Families

| Provider | Purpose |
|----------|---------|
| **Storage** | Persists task context and checkpoints (memory, file, S3, GCS, …). |
| **Notify** | Sends alerts or summaries (default no-op, Telegram, …). |
| **Log** | Structured logging for runs. |
| **Scheduler** | Drives recurring execution (default, cron with `dotflow[scheduler]`). |

You pass instances into `Config`, for example `Config(storage=StorageFile(path=".output"), scheduler=SchedulerCron(...))`. Built-in providers use **core** dependencies; cloud and cron integrations often need **pip extras**—see [Use integrations](../integrations/use-integrations.md) and the [Overview](../integrations/index.md) hub.

## Why it matters

- **Durability**: storage + [checkpoints](../tutorial/checkpoint.md) enable resume after failure.
- **Observability**: log and notify providers surface failures and retries.
- **Operations**: swap file storage in development for S3 or GCS in production with one config change.

## References

- [`Config`](../reference/config.md)
- [Custom providers](../development/custom-providers.md)
- Abstract bases: [`Storage`](../reference/abc-storage.md), [`Notify`](../reference/abc-notify.md), [`Log`](../reference/abc-log.md), [`Scheduler`](../reference/abc-scheduler.md)
