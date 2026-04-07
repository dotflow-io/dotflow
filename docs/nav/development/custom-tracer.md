# Custom Tracer

The `Tracer` provider manages distributed traces. Each workflow becomes a parent span, each task a child span.

## Methods

- `start_workflow(workflow_id, **kwargs)` — create a parent span when the workflow starts
- `end_workflow(workflow_id, **kwargs)` — close the parent span when the workflow finishes
- `start_task(task)` — create a child span when a task starts
- `end_task(task)` — close the child span when a task finishes

## Example

```python
from typing import Any

from dotflow.abc.tracer import Tracer


class TracerDatadog(Tracer):
    def __init__(self):
        from ddtrace import tracer
        self._tracer = tracer
        self._spans = {}

    def start_workflow(self, workflow_id: Any, **kwargs) -> None:
        self._spans[str(workflow_id)] = self._tracer.trace("workflow")

    def end_workflow(self, workflow_id: Any, **kwargs) -> None:
        span = self._spans.pop(str(workflow_id), None)
        if span:
            span.finish()

    def start_task(self, task: Any) -> None:
        key = f"{task.workflow_id}:{task.task_id}"
        self._spans[key] = self._tracer.trace(f"task:{task.task_id}")

    def end_task(self, task: Any) -> None:
        key = f"{task.workflow_id}:{task.task_id}"
        span = self._spans.pop(key, None)
        if span:
            span.set_tag("status", str(task.status))
            span.finish()
```

## References

- [Tracer ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-tracer/)
