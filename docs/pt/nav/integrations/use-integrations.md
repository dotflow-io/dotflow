# Usar integrações

As integrações no Dotflow são **classes de provedor** (armazenamento, notificação, log, agendador) que você passa via [`Config`](../reference/config.md) ao criar [`DotFlow`](../reference/dotflow.md). Partes opcionais vêm como **extras do pip** para manter a instalação base enxuta—no mesmo espírito da documentação do [Prefect sobre instalar integrações](https://docs.prefect.io/integrations/use-integrations).

## Instalar extras opcionais

Instale o extra correspondente com `pip` antes de importar um provedor que dependa de biblioteca de terceiros.

| Extra | Instala | Uso |
|-------|---------|-----|
| `aws` | `boto3` | [Storage S3](../tutorial/storage-s3.md) |
| `gcp` | `google-cloud-storage` | [Storage GCS](../tutorial/storage-gcs.md) |
| `scheduler` | `croniter` | [Agendador cron](../tutorial/scheduler-cron.md) |

Exemplos:

```bash
pip install "dotflow[aws]"
pip install "dotflow[gcp,scheduler]"
```

A lista oficial de extras e versões está no [`pyproject.toml`](https://github.com/dotflow-io/dotflow/blob/main/pyproject.toml), em `[project.optional-dependencies]`.

/// note
Provedores integrados (armazenamento padrão, arquivo, notify/log/agendador padrão) usam só dependências **core**—sem extra. [Telegram](../tutorial/notify-telegram.md) usa `requests`, já incluído no `dotflow`.
///

## Usar um provedor no código

1. Instale o extra (se a integração exigir).
2. Importe `Config`, `DotFlow` e o provedor de `dotflow.providers`.
3. Passe o provedor em `Config` e crie `DotFlow(config=config)`.

Exemplo mínimo com **AWS S3**:

```python
from dotflow import Config, DotFlow
from dotflow.providers import StorageS3


def step_one():
    return "ok"


config = Config(
    storage=StorageS3(
        bucket="my-dotflow-bucket",
        prefix="workflows/",
        region="us-east-1",
    )
)

workflow = DotFlow(config=config)
workflow.task.add(step=step_one)
workflow.start()
```

O mesmo padrão vale para **GCS** (`StorageGCS`), **cron** (`SchedulerCron` em `Config.scheduler`), **Telegram** (`NotifyTelegram` em `Config.notify`) e outros—cada [guia de integração](index.md) mostra argumentos e autenticação.

## Se o import falhar

Se faltar uma biblioteca, o Dotflow indica o extra (por exemplo `library="dotflow[aws]"`). Instale esse extra e execute de novo.

## Próximos passos

- [Visão geral](index.md) — todas as integrações  
- [Provedores customizados](../development/custom-providers.md) — implementar storage, notify, log ou scheduler
