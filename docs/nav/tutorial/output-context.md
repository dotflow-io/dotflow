# Output: result_context

`workflow.result_context()` returns the list of `Context` objects produced by every task in the queue. Use it when you need both the payload (`storage`) and the metadata (`time`, `task_id`, `workflow_id`) of each step.

## Function step

{* ./docs_src/output/step_function_result_context.py hl[15] *}

## Class step

A class-based step returns one `Context` whose `storage` is a list of nested contexts — one per inner `@action` method.

{* ./docs_src/output/step_class_result_context.py hl[26:27] *}

## When to use

- Auditing — full timeline of what each step produced and when
- Tracing — `task_id` and `workflow_id` propagate through the context chain
- Debugging — inspect intermediate state without rerunning

## Related

- [result_storage](output-storage.md) — bare payloads only
- [result_task](output-task.md) — full `Task` objects
