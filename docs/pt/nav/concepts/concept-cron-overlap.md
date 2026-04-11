# Sobreposição no cron

Quando o fluxo é **agendado** (por exemplo com [`SchedulerCron`](../reference/scheduler-cron.md)), uma nova execução pode disparar enquanto a anterior ainda está **`IN_PROGRESS`**. **Overlap** define o que o Dotflow faz nesse caso. As estratégias estão em [`TypeOverlap`](../reference/type-overlap.md).

## Estratégias

| Estratégia | Significado |
|------------|-------------|
| **`skip`** (padrão) | Não inicia nova execução se a anterior não terminou. |
| **`queue`** | Adia a nova execução até a anterior concluir (fila serializada). |
| **`parallel`** | Permite outra execução em paralelo (cuidado com recursos compartilhados). |

Escolher o overlap certo evita trabalho duplicado, condições de corrida e efeitos colaterais duplicados em produção.

## Onde configurar

Overlap fica no agendador (veja [Scheduler cron](../tutorial/scheduler-cron.md)). Para padrões completos (cron + storage + resume), veja [Pipeline agendado com resume](../advanced/scheduled-pipeline-with-resume.md).

## Referências

- [`TypeOverlap`](../reference/type-overlap.md)
- [`SchedulerCron`](../reference/scheduler-cron.md)
