# Keep Going on Failures

By default, a workflow stops when a task fails. Use `keep_going=True` to continue executing the remaining tasks even if one fails. Failed tasks are marked with `TypeStatus.FAILED` but do not block subsequent steps.

## Example

{* ./docs_src/workflow/keep_going_true.py *}

## References

- [Error Handling](https://dotflow-io.github.io/dotflow/nav/tutorial/error-handling/)
- [Manager](https://dotflow-io.github.io/dotflow/nav/reference/workflow/)
