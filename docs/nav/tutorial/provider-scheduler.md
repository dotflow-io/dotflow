# Scheduler Default

`SchedulerDefault` is the default scheduler provider. It does nothing — `schedule()` returns immediately without running the workflow on any recurring schedule.

This is the provider used when no scheduler is explicitly configured in `Config`. It ensures that calling `workflow.schedule()` is always safe, even when scheduling is not needed.

## Available providers

- `SchedulerDefault`: no scheduling — `schedule()` returns immediately.
- `SchedulerCron`: cron-based recurring execution using cron expressions.

## Example

{* ./docs_src/scheduler/scheduler_provider.py ln[1:25] hl[2,12,18:21] *}

## References

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
