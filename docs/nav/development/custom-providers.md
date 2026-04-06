# Custom Providers

Dotflow is designed to be extensible. Every integration point — storage, notifications, logging, and scheduling — is backed by a provider that you can replace with your own implementation.

Providers follow a simple pattern: an abstract base class (ABC) defines the contract with the methods you need to implement, and your concrete class inherits from it. Dotflow takes care of calling your provider at the right time during the workflow lifecycle.

This means you can persist task output to any database, send notifications to any channel, log to any service, or schedule workflows with any mechanism — without modifying dotflow itself.

## Available ABCs

| ABC | Import | Methods | Purpose |
|-----|--------|---------|---------|
| `Storage` | `dotflow.abc.storage` | `post()`, `get()`, `key()` | Persist and retrieve task context between steps |
| `Notify` | `dotflow.abc.notify` | `send()` | Send notifications when tasks complete or fail |
| `Log` | `dotflow.abc.log` | `info()`, `error()` | Log task status changes during execution |
| `Scheduler` | `dotflow.abc.scheduler` | `start()`, `stop()` | Control recurring workflow execution on a schedule |

## Custom Storage

The `Storage` provider is called after every task completes, saving the task context so it can be retrieved by subsequent steps or used for checkpoint-based resume.

You need to implement three methods:

- `post(key, context)` — save a context object under the given key
- `get(key)` — retrieve a context object by key, returning a `Context` with `storage=None` if not found
- `key(task)` — generate a unique key for the given task

```python
from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageRedis(Storage):
    def __init__(self, host: str = "localhost", port: int = 6379):
        import redis
        self.client = redis.Redis(host=host, port=port)

    def post(self, key: str, context: Context) -> None:
        import json
        self.client.set(key, json.dumps(context.storage))

    def get(self, key: str) -> Context:
        import json
        data = self.client.get(key)
        return Context(storage=json.loads(data) if data else None)

    def key(self, task):
        return f"{task.workflow_id}:{task.task_id}"
```

## Custom Scheduler

The `Scheduler` provider controls how and when workflows are executed on a recurring basis. The `start()` method receives the workflow callable and should block the main thread, calling it on each scheduled tick. The `stop()` method is called to shut down the loop gracefully.

- `start(workflow, **kwargs)` — start the scheduling loop, calling `workflow(**kwargs)` on each tick
- `stop()` — signal the loop to stop

```python
from collections.abc import Callable

from dotflow.abc.scheduler import Scheduler


class SchedulerInterval(Scheduler):
    def __init__(self, seconds: int = 60):
        self.seconds = seconds
        self.running = False

    def start(self, workflow: Callable, **kwargs) -> None:
        import time
        self.running = True
        while self.running:
            workflow(**kwargs)
            time.sleep(self.seconds)

    def stop(self) -> None:
        self.running = False
```

## Custom Notify

The `Notify` provider is called after each task finishes. It receives the full task object, so you can inspect its status, errors, context, and duration to decide what to send and where.

- `send(task)` — send a notification based on the task state

```python
from typing import Any

from dotflow.abc.notify import Notify


class NotifySlack(Notify):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, task: Any) -> None:
        import requests
        requests.post(self.webhook_url, json={
            "text": f"Task {task.task_id}: {task.status}"
        })
```

## Using custom providers

Pass your providers to `Config` and dotflow will use them throughout the workflow lifecycle. You can replace one, some, or all providers — anything you don't specify falls back to the default (no-op) implementation.

```python
from dotflow import Config, DotFlow

config = Config(
    storage=StorageRedis(host="redis.local"),
    scheduler=SchedulerInterval(seconds=300),
    notify=NotifySlack(webhook_url="https://hooks.slack.com/..."),
)

workflow = DotFlow(config=config)
```

/// note
Custom providers must inherit from the corresponding ABC. `Config` validates all providers at construction time with `isinstance` — passing an object that does not subclass the ABC raises `NotCallableObject`.
///

## References

- [Storage](https://dotflow-io.github.io/dotflow/nav/reference/abc-storage/)
- [Notify](https://dotflow-io.github.io/dotflow/nav/reference/abc-notify/)
- [Log](https://dotflow-io.github.io/dotflow/nav/reference/abc-log/)
- [Scheduler](https://dotflow-io.github.io/dotflow/nav/reference/abc-scheduler/)
