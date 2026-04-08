# Custom Storage

The `Storage` provider is called after every task completes, saving the task context so it can be retrieved by subsequent steps or used for checkpoint-based resume.

## Methods

- `post(key, context)` — save a context object under the given key
- `get(key)` — retrieve a context object by key, returning a `Context` with `storage=None` if not found
- `key(task)` — generate a unique key for the given task

## Example

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

## References

- [Storage ABC](https://dotflow-io.github.io/dotflow/nav/reference/abc-storage/)
