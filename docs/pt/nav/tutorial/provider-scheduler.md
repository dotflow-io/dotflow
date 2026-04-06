# Provider de Scheduler

O provider `scheduler` define como os workflows são executados de forma recorrente.

## Providers disponíveis

- `SchedulerDefault`: sem agendamento — `schedule()` retorna imediatamente.
- `SchedulerCron`: execução recorrente baseada em expressões cron.

/// note
`SchedulerCron` requer `pip install dotflow[scheduler]`
///

## Exemplo

{* ./docs_src/scheduler/scheduler_provider.py ln[1:25] hl[2,12,18:21] *}

## Referências

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
