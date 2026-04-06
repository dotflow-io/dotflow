# Scheduler Default

`SchedulerDefault` é o provider de scheduler padrão. Ele não faz nada — `schedule()` retorna imediatamente sem executar o workflow em nenhum agendamento recorrente.

Este é o provider usado quando nenhum scheduler é configurado explicitamente no `Config`. Ele garante que chamar `workflow.schedule()` é sempre seguro, mesmo quando o agendamento não é necessário.

## Providers disponíveis

- `SchedulerDefault`: sem agendamento — `schedule()` retorna imediatamente.
- `SchedulerCron`: execução recorrente baseada em expressões cron.

## Exemplo

{* ./docs_src/scheduler/scheduler_provider.py ln[1:25] hl[2,12,18:21] *}

## Referências

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
