# Scheduled Pipeline with Resume

Combine cron-based scheduling with checkpoint resume to build resilient pipelines that recover automatically from failures.

## How it works

1. `SchedulerCron` runs the workflow on a cron schedule
2. `StorageFile` (or S3/GCS) persists task output after each step
3. If a step fails, the next scheduled run skips completed steps and resumes from the failure point

## Example

{* ./docs_src/scheduler/scheduler_resume_pipeline.py hl[2,24:26,28,32] *}

## Execution flow

**Day 1 — `load` fails:**

```mermaid
graph LR
    A[extract] -->|completed| B[transform]
    B -->|completed| C[load]
    C -->|failed| D((stop))
    style A fill:#4caf50,color:#fff
    style B fill:#4caf50,color:#fff
    style C fill:#f44336,color:#fff
```

**Day 2 — automatic resume:**

```mermaid
graph LR
    A[extract] -->|skipped| B[transform]
    B -->|skipped| C[load]
    C -->|completed| D((done))
    style A fill:#9e9e9e,color:#fff
    style B fill:#9e9e9e,color:#fff
    style C fill:#4caf50,color:#fff
```

## Requirements

- A **fixed `workflow_id`** — so checkpoints persist across scheduled runs
- A **persistent storage provider** — `StorageFile`, `StorageS3`, or `StorageGCS`
- `resume=True` passed to `workflow.schedule()`

## References

- [Checkpoint](https://dotflow-io.github.io/dotflow/nav/tutorial/checkpoint/)
- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
