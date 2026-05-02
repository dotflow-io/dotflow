# Output: result_task

`workflow.result_task()` returns the full `Task` objects for every task in the queue. Each `Task` carries identity (`task_id`), execution status (`status`), error history (`errors`), and the produced context (`current_context`).

## Function step

{* ./docs_src/output/step_function_result_task.py hl[15:16] *}

## Class step

For a class-based step, the outer `Task.current_context.storage` is a list of nested `Context` objects produced by the inner `@action` methods.

{* ./docs_src/output/step_class_result_task.py hl[26:28] *}

## When to use

- Full post-mortem — task status, retry count, errors, durations
- Building dashboards / serializers (use `task.schema()` or `task.result()`)
- Driving conditional logic on `task.status` after the workflow completes

## Related

- [result_context](output-context.md) — only the produced contexts
- [result_storage](output-storage.md) — only the payloads
- [Task reference](https://dotflow-io.github.io/dotflow/nav/reference/task/)
