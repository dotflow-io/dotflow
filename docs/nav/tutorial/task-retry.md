# Task Retry

Automatically retry a task when it fails. Set `retry` on the `@action` decorator to define how many times the task should be retried before giving up.

## Retry

{* ./docs_src/retry/retry.py hl[4,12,17] *}

## Retry with Delay

Add `retry_delay` to wait a fixed number of seconds between each attempt.

{* ./docs_src/retry/retry_delay.py hl[4,12,17] *}

## References

- [Action](https://dotflow-io.github.io/dotflow/nav/reference/action/)
- [Error Handling](https://dotflow-io.github.io/dotflow/nav/tutorial/error-handling/)
