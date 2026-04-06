# Task Backoff

Use exponential backoff to increase the delay between retries. Each retry waits twice as long as the previous one. Enable it with `backoff=True` on the `@action` decorator alongside `retry` and `retry_delay`.

## Example

{* ./docs_src/backoff/backoff.py hl[4,12,17] *}

## References

- [Action](https://dotflow-io.github.io/dotflow/nav/reference/action/)
- [Task Retry](https://dotflow-io.github.io/dotflow/nav/tutorial/task-retry/)
