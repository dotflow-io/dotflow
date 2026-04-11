# Custom Scheduler

The `Scheduler` provider controls how and when workflows are executed on a recurring basis.

## Methods

- `start(workflow, **kwargs)` — start the scheduling loop, calling `workflow(**kwargs)` on each tick
- `stop()` — signal the loop to stop

## Example

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

## References

- [Scheduler ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-scheduler/)
