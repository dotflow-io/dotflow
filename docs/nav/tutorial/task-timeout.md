# Task Timeout

Set a maximum execution time for a task. If the task exceeds the timeout, it is terminated and marked as failed. Set `timeout` in seconds on the `@action` decorator.

## Example

{* ./docs_src/timeout/timeout.py hl[6,14,19] *}

## References

- [Action](https://dotflow-io.github.io/dotflow/nav/reference/action/)
- [Task Retry](https://dotflow-io.github.io/dotflow/nav/tutorial/task-retry/)
