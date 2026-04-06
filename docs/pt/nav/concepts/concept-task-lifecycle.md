# Ciclo de vida e status da tarefa

Cada tarefa passa por **status** rastreados pelo Dotflow. Eles indicam em que etapa do ciclo a execução está, incluindo retries e falhas. O enum canônico é [`TypeStatus`](../reference/type-status.md).

## Fluxo típico

1. **`NOT_STARTED`** — Na fila, ainda não executada.
2. **`IN_PROGRESS`** — Em execução.
3. **`COMPLETED`** — Concluída com sucesso; a saída vira contexto para a próxima tarefa.
4. **`FAILED`** — Terminou com erro; veja [tratamento de erros](../tutorial/error-handling.md) e observabilidade no estilo [`task.errors`](../reference/task-error.md) na API.

## Retries e pausas

- **`RETRY`** — Um retry foi agendado (por exemplo após backoff); o runner trata thread-safety no retry.
- **`PAUSED`** — Execução retida (conforme configuração do fluxo e do provedor).

A política de retry é configurada por tarefa (timeouts, backoff, etc.); veja [Retry de tarefa](../tutorial/task-retry.md) e [Backoff](../tutorial/task-backoff.md).

## Por que importa

O status alimenta callbacks, snapshots no storage e o que você mostra em logs ou UIs. Entender o enum ajuda a depurar fluxos “travados” ou loops inesperados de **`RETRY`**.

## Referências

- [`TypeStatus`](../reference/type-status.md)
- [`Task`](../reference/task.md)
- [Timeout de tarefa](../tutorial/task-timeout.md)
