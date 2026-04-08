# Cron overlap

When a workflow is **scheduled** (for example with [`SchedulerCron`](../reference/scheduler-cron.md)), a new run may be triggered while the previous one is still **`IN_PROGRESS`**. **Overlap** defines what Dotflow should do in that case. Strategies are defined by [`TypeOverlap`](../reference/type-overlap.md).

## Strategies

| Strategy | Meaning |
|----------|---------|
| **`skip`** (default) | Do not start a new run if the previous run has not finished. |
| **`queue`** | Defer the new run until the previous completes (serialized backlog). |
| **`parallel`** | Allow another run to start concurrently (use with care for shared resources). |

Choosing the right overlap avoids double work, database races, and duplicate side effects in production pipelines.

## Where to configure

Overlap is set on the scheduler (see [Scheduler cron](../tutorial/scheduler-cron.md)). For end-to-end patterns (cron + storage + resume), see [Scheduled pipeline with resume](../advanced/scheduled-pipeline-with-resume.md).

## References

- [`TypeOverlap`](../reference/type-overlap.md)
- [`SchedulerCron`](../reference/scheduler-cron.md)
