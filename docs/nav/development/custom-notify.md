# Custom Notify

The `Notify` provider is called when a task status changes. It receives the full task object, so you can inspect its status, errors, context, and duration to decide what to send and where.

## Methods

- `hook_status_task(task)` — hook called when a task status changes

## Example

```python
from typing import Any

from dotflow.abc.notify import Notify


class NotifySlack(Notify):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def hook_status_task(self, task: Any) -> None:
        import requests
        requests.post(self.webhook_url, json={
            "text": f"Task {task.task_id}: {task.status}"
        })
```

## References

- [Notify ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-notify/)
