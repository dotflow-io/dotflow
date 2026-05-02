# With Resume

The `--resume` flag tells `dotflow start` to skip tasks that already have a checkpoint in the configured storage.

## Usage

```bash
dotflow start --workflow docs_src.cli.cli_with_workflow:pipeline --resume
```

## When to use

- A previous run failed mid-pipeline and you fixed the root cause
- A long-running pipeline was killed by infra (Lambda timeout, OOM, instance preemption)
- You want to verify a specific step in isolation without re-running upstream

## Requirements

- A **fixed `workflow_id`** so dotflow can locate the previous checkpoints
- A **persistent storage provider** (`StorageFile`, `StorageS3`, `StorageGCS`)

Set `WORKFLOW_ID` via environment, or expose it inside the workflow factory.

```bash
WORKFLOW_ID=12345678-1234-5678-1234-567812345678 \
  dotflow start --workflow docs_src.cli.cli_with_workflow:pipeline --resume
```

## Combine with `--step`

`--resume` works with a single-step entry as well:

```bash
dotflow start --step docs_src.cli.cli_with_workflow:step_one --resume
```

## Input change

If the `initial_context` differs from the stored checkpoint, the behavior is controlled by `on_input_change` (see [Checkpoint with input-change policy](../tutorial/checkpoint-input-change.md)).

## References

- [Checkpoint](https://dotflow-io.github.io/dotflow/nav/tutorial/checkpoint/)
- [With Workflow](./with-workflow.md)
