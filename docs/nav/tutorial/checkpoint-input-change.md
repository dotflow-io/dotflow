# Checkpoint with input-change policy

`resume=True` skips tasks that already have a checkpoint. But what happens when the **input changed** between runs? Without an explicit policy, the old checkpoint silently wins and the new payload is ignored — a common footgun in queued/job-based deployments.

`on_input_change` makes that behavior explicit.

## How it works

1. On each `start()`, dotflow computes a fingerprint of `initial_context` and stores it next to the checkpoints
2. On the next run, the stored fingerprint is compared with the current one
3. If they differ, dotflow applies the policy you chose

## Policies

| Policy | Behavior |
|--------|----------|
| `reuse` | Keep checkpoints, ignore input change (legacy behavior, default) |
| `reset` | Invalidate checkpoints and re-run from scratch |
| `raise` | Raise `InputChangedError` and force the caller to decide |

## Example

{* ./docs_src/checkpoint/checkpoint_input_change.py hl[32] *}

## When to use each policy

- **`reset`** — input drives the result. Same job key with new payload should re-process. Common in ETL where `customer_id` is stable but the dataset grows.
- **`raise`** — operator must approve. Useful in financial / regulated pipelines where a silent re-run would be unsafe.
- **`reuse`** — input is informational. Defaults preserve current behavior for existing pipelines.

## Custom fingerprint

Pass an explicit `fingerprint=` to override the automatic computation. Useful when the payload contains volatile fields (timestamps, request IDs) that should not invalidate the checkpoint.

```python
fp = sha256(payload["s3_key"].encode()).hexdigest()
workflow.start(resume=True, on_input_change="reset", fingerprint=fp)
```

## References

- [Checkpoint](https://dotflow-io.github.io/dotflow/nav/tutorial/checkpoint/)
- [Issue #281](https://github.com/dotflow-io/dotflow/issues/281)
