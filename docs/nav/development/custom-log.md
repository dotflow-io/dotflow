# Custom Log

The `Log` ABC provides built-in formatting (`simple` and `json`), level filtering, and dispatch. Subclasses only need to configure `self._logger`, `self._level`, and `self._format` in their `__init__`.

## Built-in behavior

The ABC handles:

- **Level filtering** — messages below `self._level` are skipped
- **Formatters** — `simple` (plain text) and `json` (structured via `LogRecord` model)
- **Dispatch** — `info`, `error`, `warning`, `debug` all delegate to `_log`

All methods receive `task=` as a keyword argument when called from the task lifecycle.

## JSON format

The `json` formatter uses Pydantic models for structured output:

- `LogRecord` — timestamp, level, workflow_id, task_id, status, duration, retry_count, error
- `LogRecordError` — exception, message

## Example

Minimal custom provider — just set up the logger:

```python
import logging

from dotflow.abc.log import LEVELS, Log


class LogStructured(Log):
    def __init__(self, level: str = "INFO", format: str = "simple"):
        self._level = LEVELS.get(level.upper(), logging.INFO)
        self._format = format

        self._logger = logging.getLogger("dotflow.structured")
        self._logger.setLevel(self._level)
        self._logger.handlers.clear()
        self._logger.propagate = False
        self._logger.addHandler(logging.StreamHandler())
```

Override formatting if you need custom behavior:

```python
import logging

from dotflow.abc.log import LEVELS, Log


class LogCustomFormat(Log):
    def __init__(self, level: str = "INFO"):
        self._level = LEVELS.get(level.upper(), logging.INFO)
        self._format = "simple"

        self._logger = logging.getLogger("dotflow.custom")
        self._logger.setLevel(self._level)
        self._logger.handlers.clear()
        self._logger.propagate = False
        self._logger.addHandler(logging.StreamHandler())

    def _format_text(self, level: int, **kwargs) -> str:
        task = kwargs.get("task")
        if task:
            return f"[{task.workflow_id}] task:{task.task_id} {task.status}"
        return str(kwargs)
```

## References

- [Log ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-log/)
