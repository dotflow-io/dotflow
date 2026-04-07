# Custom Providers

Dotflow is designed to be extensible. Every integration point — storage, notifications, logging, scheduling, tracing, and metrics — is backed by a provider that you can replace with your own implementation.

Providers follow a simple pattern: an abstract base class (ABC) defines the contract with the methods you need to implement, and your concrete class inherits from it. Dotflow takes care of calling your provider at the right time during the workflow lifecycle.

## Available ABCs

| ABC | Import | Methods | Purpose |
|-----|--------|---------|---------|
| `Storage` | `dotflow.abc.storage` | `post()`, `get()`, `key()` | Persist and retrieve task context between steps |
| `Notify` | `dotflow.abc.notify` | `hook_status_task()` | Hook called when a task status changes |
| `Log` | `dotflow.abc.log` | `info()`, `error()`, `warning()`, `debug()` | Log task and workflow events |
| `Scheduler` | `dotflow.abc.scheduler` | `start()`, `stop()` | Control recurring workflow execution |
| `Tracer` | `dotflow.abc.tracer` | `start_workflow()`, `end_workflow()`, `start_task()`, `end_task()` | Distributed tracing with spans |
| `Metrics` | `dotflow.abc.metrics` | `workflow_started()`, `workflow_completed()`, `workflow_failed()`, `task_completed()`, `task_failed()`, `task_retried()` | Counters and histograms |

## Using custom providers

Pass your providers to `Config` and dotflow will use them throughout the workflow lifecycle. You can replace one, some, or all providers — anything you don't specify falls back to the default (no-op) implementation.

```python
from dotflow import Config, DotFlow

config = Config(
    storage=StorageRedis(host="redis.local"),
    notify=NotifySlack(webhook_url="https://hooks.slack.com/..."),
    scheduler=SchedulerInterval(seconds=300),
    tracer=TracerDatadog(),
    metrics=MetricsStatsd(host="statsd.local"),
)

workflow = DotFlow(config=config)
```

/// note
Custom providers must inherit from the corresponding ABC. `Config` validates all providers at construction time with `isinstance` — passing an object that does not subclass the ABC raises `NotCallableObject`.
///
