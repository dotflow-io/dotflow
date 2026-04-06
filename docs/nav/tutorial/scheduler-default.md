# Scheduler Default

`SchedulerDefault` is the default scheduler provider. It does nothing — `schedule()` returns immediately without running the workflow on any recurring schedule.

This is the provider used when no scheduler is explicitly configured in `Config`. It ensures that calling `workflow.schedule()` is always safe, even when scheduling is not needed.

## Example

{* ./docs_src/scheduler/scheduler_default.py hl[2,11] *}

## References

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
