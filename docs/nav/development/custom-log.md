# Custom Log

The `Log` provider is called on task status changes to record execution events. `info` and `error` are required; `warning` and `debug` are optional.

## Methods

- `info(**kwargs)` — called on task status change (required)
- `error(**kwargs)` — called on task failure (required)
- `warning(**kwargs)` — called on retry (optional, no-op by default)
- `debug(**kwargs)` — available for custom use (optional, no-op by default)

All methods receive `task=` as a keyword argument when called from the task lifecycle. Additional kwargs may be passed for workflow-level events.

## Example

```python
import logging

from dotflow.abc.log import Log


class LogStructured(Log):
    def __init__(self):
        self._logger = logging.getLogger("dotflow.structured")

    def info(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.info(f"[{task.workflow_id}] task:{task.task_id} {task.status}")

    def error(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.error(f"[{task.workflow_id}] task:{task.task_id} FAILED")

    def warning(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._logger.warning(f"[{task.workflow_id}] task:{task.task_id} RETRY")
```

## References

- [Log ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-log/)
