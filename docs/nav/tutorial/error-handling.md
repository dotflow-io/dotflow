# Error Handling

## Accessing Errors

Each task tracks all errors that occur during execution, including retry attempts and the final failure. Errors are stored in `task.errors` as a list of `TaskError` objects.

Each `TaskError` contains:

| Attribute   | Type         | Description                                      |
|-------------|--------------|--------------------------------------------------|
| `attempt`   | `int | None` | Which attempt triggered the error (retry errors)  |
| `exception` | `str`        | Exception class name (e.g. `"ValueError"`)        |
| `message`   | `str`        | Error message                                     |
| `traceback` | `str`        | Full traceback string                             |

## Example

{* ./docs_src/errors/errors.py hl[4,16,17,20] *}

## Output

```
Retry count: 2
Total errors: 3
  Attempt 1: [ValueError] Something went wrong
  Attempt 2: [ValueError] Something went wrong
  Attempt None: [ValueError] Something went wrong
```

The first two errors come from retry attempts (with `attempt` set). The last error is the final failure recorded by the execution engine (no `attempt` since it's not a retry).

## Accessing the Last Error

To get only the final error:

```python
task = workflow.result_task()[0]
if task.errors:
    last = task.errors[-1]
    print(last.message)
    print(last.exception)
    print(last.traceback)
```

/// warning
`task.error` is deprecated. Use `task.errors` instead.
///
