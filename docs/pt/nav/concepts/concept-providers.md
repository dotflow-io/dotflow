# Provedores

**Provedores** são backends plugáveis ligados via [`Config`](../reference/config.md). Permitem usar o mesmo código de fluxo com armazenamento, notificações, log e agendamento diferentes, sem mudar a lógica das tarefas.

## Famílias

| Provedor | Função |
|----------|--------|
| **Storage** | Persiste contexto e checkpoints (memória, arquivo, S3, GCS, …). |
| **Notify** | Alertas ou resumos (padrão no-op, Telegram, …). |
| **Log** | Registro estruturado das execuções. |
| **Scheduler** | Execução recorrente (padrão, cron com `dotflow[scheduler]`). |

Você passa instâncias em `Config`, por exemplo `Config(storage=StorageFile(path=".output"), scheduler=SchedulerCron(...))`. Provedores integrados usam dependências **core**; nuvem e cron costumam exigir **extras do pip**—veja [Usar integrações](../integrations/use-integrations.md) e o hub [Visão geral](../integrations/index.md).

## Por que importa

- **Durabilidade**: storage + [checkpoints](../tutorial/checkpoint.md) permitem retomar após falha.
- **Observabilidade**: log e notify expõem falhas e retries.
- **Operação**: trocar arquivo em desenvolvimento por S3 ou GCS em produção mudando só a config.

## Referências

- [`Config`](../reference/config.md)
- [Provedores customizados](../development/custom-providers.md)
- Bases abstratas: [`Storage`](../reference/abc-storage.md), [`Notify`](../reference/abc-notify.md), [`Log`](../reference/abc-log.md), [`Scheduler`](../reference/abc-scheduler.md)
