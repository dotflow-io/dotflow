# Task Engine

The `TaskEngine` manages the **lifecycle** of a single task — status transitions, duration tracking, retry, timeout, backoff, error handling, and tracer integration. Execution strategies (`Sequential`, `Parallel`, etc.) are responsible only for **ordering and parallelism**.

## Architecture

```mermaid
sequenceDiagram
    participant S as Strategy
    participant E as TaskEngine
    participant A as @action

    S->>E: TaskEngine(task, workflow_id, previous_context)
    S->>E: with engine.start()
    E->>E: status = IN_PROGRESS
    E->>E: tracer.start_task()
    S->>E: engine.execute_with_retry()

    loop retry loop (max_attempts)
        alt timeout > 0
            E->>E: _execute_with_timeout()
        else no timeout
            E->>E: _execute_single()
        end
        E->>A: task.step()
        alt success
            A-->>E: Context
            E-->>S: result
        else failure & attempts remaining
            E->>E: status = RETRY
            E->>E: sleep(delay)
        end
    end

    E->>E: status = COMPLETED / FAILED
    E->>E: tracer.end_task()
    S->>S: task.callback()
    S->>S: _flow_callback()
```

## How it works

The engine uses a **context manager** pattern to separate lifecycle from execution:

```python
engine = TaskEngine(task=task, workflow_id=workflow_id, previous_context=previous_context)

with engine.start():
    engine.execute_with_retry()
```

### `start()` — lifecycle context manager

Manages everything that happens **around** the execution:

```mermaid
stateDiagram-v2
    [*] --> IN_PROGRESS: start()
    IN_PROGRESS --> COMPLETED: success
    IN_PROGRESS --> RETRY: retry attempt
    RETRY --> COMPLETED: success after retry
    RETRY --> FAILED: max attempts reached
    IN_PROGRESS --> FAILED: exception
    COMPLETED --> [*]: end_task tracer
    FAILED --> [*]: end_task tracer
```

1. Sets `status = IN_PROGRESS` and starts the timer
2. Starts the tracer span
3. **Yields** — the execution block runs here
4. On success: sets `duration` and `status = COMPLETED`
5. On error: sets `errors` and `status = FAILED`
6. Always: ends the tracer span

### `execute_with_retry()` — retry, timeout, and backoff

Reads `retry`, `timeout`, `retry_delay`, and `backoff` from the `@action` decorator and manages the full retry loop:

```mermaid
flowchart TD
    A["execute_with_retry()"] --> B{"timeout > 0?"}
    B -->|yes| C["_execute_with_timeout()"]
    B -->|no| D["_execute_single()"]
    C --> E{"success?"}
    D --> E
    E -->|yes| F["return result"]
    E -->|no| G{"attempt < max?"}
    G -->|yes| H["status = RETRY\nsleep(delay)"]
    H -->|"backoff?"| I["delay *= 2"]
    I --> B
    H -->|no backoff| B
    G -->|no| J["raise exception"]
```

- If `timeout > 0`: uses `ThreadPoolExecutor` with a real deadline
- If execution fails and `attempt < max_attempts`: sets `status = RETRY`, waits, and retries
- If `backoff = True`: doubles the delay after each failed attempt

### `execute()` — single execution

Calls the task function once without retry. Used internally by `execute_with_retry()` and available for cases where retry is not needed.

## References

- [Task lifecycle and status](concept-task-lifecycle.md)
- [`@action` decorator](../reference/action.md)
- [`TypeStatus`](../reference/type-status.md)
