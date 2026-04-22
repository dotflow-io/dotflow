# Server Default

`ServerDefault` is the built-in Server provider. It auto-detects managed mode from the CLI config file or environment variables — when a `base_url` and `token` are available, it sends execution data to the remote API. Without them, all methods are no-ops.

## Managed mode (auto-detected)

There are two ways to feed the provider.

### 1. `dotflow login` (recommended)

Run the device-authorization flow once and the CLI stores `base_url` + `token` in `~/.dotflow/config.json`:

```bash
dotflow login
```

Any subsequent `DotFlow()` instance picks those up automatically — no env vars, no code changes:

```python
from dotflow import DotFlow


def main() -> DotFlow:
    workflow = DotFlow()
    workflow.task.add(step=my_step)

    return workflow
```

### 2. Environment variables (CI/CD)

For non-interactive environments, export the variables directly:

```bash
export SERVER_BASE_URL="https://api.example.com/v1"
export SERVER_USER_TOKEN="your-token"
```

Env vars take precedence over the config file.

## Lifecycle hooks

The server provider is called automatically at these points:

| Event | Method |
|-------|--------|
| `DotFlow()` init | `create_workflow()` |
| `workflow.start()` | `update_workflow()` |
| Workflow completes | `update_workflow()` |
| `task.add()` | `create_task()` |
| Task finishes | `update_task()` |

Requests hit `{base_url}/cli/workflows/*` with `Authorization: Bearer <token>`.

## Custom implementation

To build your own server provider, extend the `Server` ABC:

```python
from dotflow.abc.server import Server


class MyServer(Server):
    def create_workflow(self, workflow):
        pass

    def update_workflow(self, workflow, status=""):
        pass

    def create_task(self, task):
        pass

    def update_task(self, task):
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
