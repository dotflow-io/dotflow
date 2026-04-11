# Server Default

Sends real-time workflow and task execution data to a remote API (such as [dotflow-api](https://github.com/dotflow-io/dotflow-api)).

When enabled, dotflow automatically reports workflow creation, status transitions, task results, and errors via HTTP.

## Install

```bash
pip install requests
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | `str` | `""` | Base URL of the API (e.g. `http://localhost:8000/api/v1`) |
| `user_token` | `str` | `""` | API authentication token sent as `X-User-Token` header |
| `timeout` | `float` | `5.0` | HTTP request timeout in seconds |

The provider is automatically **disabled** when `base_url` or `user_token` is empty.

## Basic usage

{* ./docs_src/server/server_default.py hl[2,27:30] *}

## With retry and error tracking

{* ./docs_src/server/server_with_retry.py hl[13,27:30] *}

## Combined with storage

{* ./docs_src/server/server_with_storage.py hl[3,24:28] *}

## Lifecycle hooks

The server provider is called automatically at these points:

| Event | Method | HTTP |
|-------|--------|------|
| `DotFlow()` init | `create_workflow()` | `POST /workflows` |
| `workflow.start()` | `update_workflow()` | `PATCH /workflows/{id}` |
| Workflow completes | `update_workflow()` | `PATCH /workflows/{id}` |
| `task.add()` | `create_task()` | `POST /workflows/{id}/tasks` |
| Task finishes | `update_task()` | `PATCH /workflows/{id}/tasks/{id}` |

## References

- [ServerDefault](../reference/server-default.md)
- [Server ABC](../reference/abc-server.md)
