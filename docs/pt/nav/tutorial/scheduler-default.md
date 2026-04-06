# Scheduler Default

`SchedulerDefault` é o provider de scheduler padrão. Ele não faz nada — `schedule()` retorna imediatamente sem executar o workflow em nenhum agendamento recorrente.

Este é o provider usado quando nenhum scheduler é configurado explicitamente no `Config`. Ele garante que chamar `workflow.schedule()` é sempre seguro, mesmo quando o agendamento não é necessário.

## Exemplo

{* ./docs_src/scheduler/scheduler_default.py hl[2,11] *}

## Referências

- [SchedulerDefault](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-default/)
