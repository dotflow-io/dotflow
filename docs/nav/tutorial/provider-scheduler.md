# Scheduler Provider

The `scheduler` provider defines how workflows are executed on a recurring schedule.

## Available providers

- `SchedulerDefault`: no scheduling — `schedule()` returns immediately.
- `SchedulerCron`: cron-based recurring execution using cron expressions.

/// note
`SchedulerCron` requires `pip install dotflow[scheduler]`
///

## Example

{* ./docs_src/scheduler/scheduler_provider.py ln[1:25] hl[2,12,18:21] *}

## References

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
