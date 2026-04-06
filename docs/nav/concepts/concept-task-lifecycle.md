# Task lifecycle and status

Every task moves through **status** values tracked by Dotflow. They describe where a step is in its lifetime, including retries and failures. The canonical enum is [`TypeStatus`](../reference/type-status.md).

## Typical flow

1. **`NOT_STARTED`** — Queued but not yet executed.
2. **`IN_PROGRESS`** — Currently running.
3. **`COMPLETED`** — Finished successfully; output is available as context for the next task.
4. **`FAILED`** — Finished with an error; see [error handling](../tutorial/error-handling.md) and [`task.errors`](../reference/task-error.md)-style observability in the API.

## Retries and pauses

- **`RETRY`** — A retry is scheduled (for example after backoff); thread-safe retry behavior is part of the action runner.
- **`PAUSED`** — Execution is held (depending on workflow configuration and provider behavior).

Retry policy is configured per task (timeouts, backoff, etc.); see [Task retry](../tutorial/task-retry.md) and [Task backoff](../tutorial/task-backoff.md).

## Why it matters

Status drives callbacks, storage snapshots, and what you show in logs or UIs. Understanding the enum helps when debugging “stuck” workflows or unexpected **`RETRY`** loops.

## References

- [`TypeStatus`](../reference/type-status.md)
- [`Task`](../reference/task.md)
- [Task timeout](../tutorial/task-timeout.md)
