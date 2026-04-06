# Async Actions

Dotflow supports `async def` actions for I/O-bound tasks like HTTP calls, database queries, and file operations.

## Example

{* ./docs_src/async/async_action.py hl[7,13,19] *}

## How it works

When an action is an `async def` function, dotflow detects it automatically and runs it with `asyncio.run()`. No changes needed in the workflow — just use `async def` instead of `def`.

```python
# Sync — blocks the thread while waiting
@action
def step_sync():
    return requests.get("https://api.com").json()

# Async — frees the thread while waiting
@action
async def step_async():
    async with aiohttp.ClientSession() as session:
        resp = await session.get("https://api.com")
        return await resp.json()
```

## Mixing sync and async

You can mix sync and async actions in the same workflow:

```python
workflow = DotFlow()
workflow.task.add(step=async_step)   # async
workflow.task.add(step=sync_step)    # sync
workflow.task.add(step=async_step)   # async
workflow.start()
```

## Retry and timeout

Retry, timeout, and backoff work the same way with async actions:

```python
@action(retry=3, timeout=30, backoff=True)
async def unreliable_api():
    async with aiohttp.ClientSession() as session:
        resp = await session.get("https://api.com/data")
        return await resp.json()
```

## When to use async

| Scenario | Use async? |
|----------|-----------|
| HTTP calls | Yes |
| Database queries | Yes |
| File I/O | Yes |
| CPU-bound computation | No — use sync |
| Simple data transformation | No — use sync |

## References

- [Action](https://dotflow-io.github.io/dotflow/nav/reference/action/)
- [Task Retry](https://dotflow-io.github.io/dotflow/nav/tutorial/task-retry/)
