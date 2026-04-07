# Custom Metrics

The `Metrics` provider records counters and histograms for workflow and task execution.

## Methods

- `workflow_started(workflow_id, **kwargs)` — increment workflow counter
- `workflow_completed(workflow_id, duration)` — record successful workflow duration
- `workflow_failed(workflow_id, duration)` — record failed workflow duration
- `task_completed(task)` — increment task success counter
- `task_failed(task)` — increment task failure counter
- `task_retried(task)` — increment retry counter

## Example

```python
from typing import Any

from dotflow.abc.metrics import Metrics


class MetricsStatsd(Metrics):
    def __init__(self, host: str = "localhost", port: int = 8125):
        from statsd import StatsClient
        self._client = StatsClient(host, port)

    def workflow_started(self, workflow_id: Any, **kwargs) -> None:
        self._client.incr("dotflow.workflow.started")

    def workflow_completed(self, workflow_id: Any, duration: float) -> None:
        self._client.incr("dotflow.workflow.completed")
        self._client.timing("dotflow.workflow.duration", duration * 1000)

    def workflow_failed(self, workflow_id: Any, duration: float) -> None:
        self._client.incr("dotflow.workflow.failed")

    def task_completed(self, task: Any) -> None:
        self._client.incr("dotflow.task.completed")

    def task_failed(self, task: Any) -> None:
        self._client.incr("dotflow.task.failed")

    def task_retried(self, task: Any) -> None:
        self._client.incr("dotflow.task.retried")
```

## References

- [Metrics ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-metrics/)
