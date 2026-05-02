# Output: result_storage

`workflow.result_storage()` returns only the payloads (`Context.storage`) of each task — no metadata. Use it when downstream code consumes raw data and metadata is noise.

## Function step

{* ./docs_src/output/step_function_result_storage.py hl[15] *}

## Class step

A class-based step yields a list of nested `Context` objects in `storage`. Iterate twice to reach the inner payloads.

{* ./docs_src/output/step_class_result_storage.py hl[26:27] *}

## When to use

- Pure data hand-off to a downstream system (DB insert, API push)
- Asserting payload shape in tests without unwrapping `Context`
- Forwarding step output to a non-dotflow consumer

## Related

- [result_context](output-context.md) — payload + metadata
- [result_task](output-task.md) — full `Task` objects
