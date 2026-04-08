# Fluxo de trabalho e tarefas

Um **fluxo de trabalho** no Dotflow é um conjunto ordenado de **tarefas** montado em uma instância de [`DotFlow`](../reference/dotflow.md). Você registra passos com `workflow.task.add(...)` e executa com **`start`** (execução pontual) ou **`schedule`** (execuções recorrentes quando há agendador configurado).

## Peças principais

| Peça | Papel |
|------|--------|
| [`DotFlow`](../reference/dotflow.md) | Ponto de entrada: `config`, `workflow_id` e o construtor de tarefas. |
| [`TaskBuilder`](../reference/task-builder.md) | Acumula tarefas na fila antes da execução. |
| [`Manager`](../reference/workflow.md) | Executa a fila (sequencial, em segundo plano ou paralelo) e coordena storage e callbacks. |
| **Action** | Callable com [`@action`](../reference/decorators.md); o Dotflow trata como unidade de trabalho com contexto de entrada/saída. |

Cada tarefa consome o **contexto anterior** do passo anterior e pode emitir um novo **contexto** para a próxima. Veja [Conceito de contexto](concept-of-context.md) e os guias [Contexto inicial](../tutorial/initial-context.md) e [Contexto anterior](../tutorial/previous-context.md).

## Execução vs agendamento

- **`start`** roda o fluxo na hora (veja [Modo de processamento](process-mode-sequential.md) para *como* as tarefas são ordenadas e paralelizadas).
- **`schedule`** delega ao **agendador** configurado (por exemplo cron); a sobreposição entre execuções é controlada por [estratégias de overlap](concept-cron-overlap.md).

## Referências

- [`DotFlow`](../reference/dotflow.md)
- [`Task`](../reference/task.md)
- [Primeiros passos](../tutorial/first-steps.md)
