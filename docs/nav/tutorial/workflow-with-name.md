# Workflow with name

`DotFlow` accepts an optional `name` kwarg that labels the workflow on the managed server. When omitted, the name defaults to the machine hostname — useful to distinguish runs from different hosts in the dashboard.

## Why set a name

- **Dashboard clarity** — runs grouped by purpose (`etl-nightly`, `report-monthly`) instead of by host
- **Idempotent start** — combined with a fixed `workflow_id`, a re-run of the same `DotFlow` instance returns the existing `Manager` instead of starting a duplicate
- **Search / filter** — managed-mode users can find runs by human-readable label

## Example

{* ./docs_src/name/workflow_with_name.py hl[18] *}

## Default behavior

Without `name`, dotflow uses `socket.gethostname()`:

```python
workflow = DotFlow()  # name = "macbook-pro.local" (or similar)
```

This is fine for ad-hoc local runs. For production pipelines, prefer an explicit semantic label.

## Idempotent start

`DotFlow.start()` is idempotent for a given task signature. Calling `start()` twice on the same instance returns the original `Manager` and logs a warning:

```python
workflow = DotFlow(name="etl-nightly")
workflow.task.add(step=step_one)
m1 = workflow.start()
m2 = workflow.start()  # warns: duplicate call ignored
assert m1 is m2
```

This protects against double-execution when the same factory is invoked twice in a job runner.

## References

- [DotFlow](https://dotflow-io.github.io/dotflow/nav/reference/dotflow/)
