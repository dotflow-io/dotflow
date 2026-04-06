# Scheduler Cron

Execute workflows de forma recorrente usando expressões cron. Sem ferramentas externas — tudo fica em Python.

/// note
Requer `pip install dotflow[scheduler]`
///

## Exemplo

{* ./docs_src/scheduler/scheduler_cron.py hl[4,17,24] *}

## Com resume

Combine agendamento com checkpoint. Se uma execução falhar, a próxima execução agendada continua do último passo concluído.

{* ./docs_src/scheduler/scheduler_resume.py hl[22:24,32] *}

## Estratégias de overlap

Controla o que acontece quando uma nova execução é disparada enquanto a anterior ainda está rodando.

| Estratégia | Comportamento |
|------------|---------------|
| `skip` (padrão) | Se a execução anterior ainda está ativa, pula esta execução |
| `queue` | Enfileira a execução, roda quando a anterior terminar |
| `parallel` | Roda independentemente, mesmo se a anterior ainda estiver ativa |

{* ./docs_src/scheduler/scheduler_overlap.py ln[13:28] hl[15,19,23] *}

## Fluxo de execução

**skip — cron a cada 5 min, tarefa leva 7 min:**

```mermaid
graph LR
    A["00:00 — executa"] -->|rodando| B["00:05 — pula"]
    B -->|ainda rodando| C["00:10 — executa"]
    style A fill:#4caf50,color:#fff
    style B fill:#9e9e9e,color:#fff
    style C fill:#4caf50,color:#fff
```

**queue — cron a cada 5 min, tarefa leva 7 min:**

```mermaid
graph LR
    A["00:00 — executa"] -->|rodando| B["00:05 — enfileirado"]
    B -->|"executa ~00:07"| C["00:10 — enfileirado"]
    style A fill:#4caf50,color:#fff
    style B fill:#ff9800,color:#fff
    style C fill:#ff9800,color:#fff
```

**parallel — cron a cada 5 min, tarefa leva 7 min:**

```mermaid
graph LR
    A["00:00 — executa"] -->|rodando| B["00:05 — executa"]
    B -->|ambos rodando| C["00:10 — executa"]
    style A fill:#4caf50,color:#fff
    style B fill:#4caf50,color:#fff
    style C fill:#4caf50,color:#fff
```

## Desligamento gracioso

O scheduler escuta sinais `SIGINT` (Ctrl+C) e `SIGTERM`. Quando recebido, a execução atual termina e o scheduler para de forma limpa.

## Referências

- [SchedulerCron](https://dotflow-io.github.io/dotflow/nav/reference/scheduler-cron/)
- [Checkpoint](https://dotflow-io.github.io/dotflow/nav/tutorial/checkpoint/)
