# Server Default

The default Server provider is a **no-op** — all methods do nothing. It serves as a safe placeholder so the workflow lifecycle can call server hooks without errors when no remote server is configured.

To send execution data to a remote API, implement a custom provider that extends the [`Server`](../reference/abc-server.md) ABC.

## Lifecycle hooks

The server provider is called automatically at these points:

| Event | Method |
|-------|--------|
| `DotFlow()` init | `create_workflow()` |
| `workflow.start()` | `update_workflow()` |
| Workflow completes | `update_workflow()` |
| `task.add()` | `create_task()` |
| Task finishes | `update_task()` |

## Custom implementation

To build your own server provider, extend the `Server` ABC:

```python
from dotflow.abc.server import Server


class MyServer(Server):
    def create_workflow(self, workflow):
        # POST to your API
        pass

    def update_workflow(self, workflow, status=""):
        # PATCH workflow status
        pass

    def create_task(self, task):
        # POST task data
        pass

    def update_task(self, task):
        # PATCH task results
        pass
```

Then pass it to `Config`:

```python
from dotflow import Config, DotFlow

config = Config(server=MyServer())
workflow = DotFlow(config=config)
```

## References

- [ServerDefault](../reference/server-default.md)
- [Server ABC](../reference/abc-server.md)
- [Custom Providers](../development/custom-providers.md)
