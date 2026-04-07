# Use integrations

Integrations in Dotflow are **provider classes** (storage, notify, log, scheduler) that you pass through [`Config`](../reference/config.md) when creating [`DotFlow`](../reference/dotflow.md). Optional pieces ship as **pip extras** so the base install stays small—similar in spirit to how [Prefect documents installing integration packages](https://docs.prefect.io/integrations/use-integrations).

## Install optional extras

Install the matching extra with `pip` before importing a provider that needs a third-party library.

| Extra | Installs | Use for |
|-------|----------|---------|
| `aws` | `boto3` | [Storage S3](../tutorial/storage-s3.md) |
| `gcp` | `google-cloud-storage` | [Storage GCS](../tutorial/storage-gcs.md) |
| `scheduler` | `croniter` | [Scheduler cron](../tutorial/scheduler-cron.md) |
| `otel` | `opentelemetry-api`, `opentelemetry-sdk` | [Tracer](../tutorial/tracer-opentelemetry.md), [Metrics](../tutorial/metrics-opentelemetry.md) |

Examples:

```bash
pip install "dotflow[aws]"
pip install "dotflow[gcp,scheduler]"
```

The authoritative list of extras and pinned versions lives in [`pyproject.toml`](https://github.com/dotflow-io/dotflow/blob/main/pyproject.toml) under `[project.optional-dependencies]`.

/// note
Built-in providers (default storage, file storage, default notify/log/scheduler) use only **core** dependencies—no extra needed. [Telegram](../tutorial/notify-telegram.md) and [Discord](../tutorial/notify-discord.md) use `requests`, which is already a dependency of `dotflow`.
///

## Use a provider in code

1. Install the extra (if that integration requires one).
2. Import `Config`, `DotFlow`, and the provider from `dotflow.providers`.
3. Pass the provider into `Config`, then build `DotFlow(config=config)`.

Minimal **AWS S3** example:

```python
from dotflow import Config, DotFlow
from dotflow.providers import StorageS3


def step_one():
    return "ok"


config = Config(
    storage=StorageS3(
        bucket="my-dotflow-bucket",
        prefix="workflows/",
        region="us-east-1",
    )
)

workflow = DotFlow(config=config)
workflow.task.add(step=step_one)
workflow.start()
```

The same pattern applies to **GCS** (`StorageGCS`), **cron** (`SchedulerCron` on `Config.scheduler`), **Telegram** (`NotifyTelegram` on `Config.notify`), **Discord** (`NotifyDiscord` on `Config.notify`), and other providers—each [integration guide](index.md) shows the exact constructor arguments and auth model.

## If import fails

If a provider needs a library you did not install, Dotflow raises a clear error pointing at the extra (for example `library="dotflow[aws]"`). Install that extra and run again.

## Next steps

- [Overview](index.md) — all integrations at a glance  
- [Custom providers](../development/custom-providers.md) — implement your own storage, notify, log, or scheduler backend
