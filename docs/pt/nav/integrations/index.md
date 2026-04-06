# Visão geral

Esta página lista as **integrações** do Dotflow com **fornecedores externos** (armazenamento em nuvem, APIs de mensagens) e com provedores **integrados**, sem conta de terceiros. Há **extras opcionais** quando necessário (por exemplo `pip install dotflow[aws]`). Cada card leva a um guia; a API está em **Referência → Provedores**. Para instalar extras e usar `Config`, comece em **[Usar integrações](use-integrations.md)**.

## AWS

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-aws: __Amazon S3__

    ---

    Estado durável do fluxo no **AWS S3** para nuvem e serverless.

    [:octicons-arrow-right-24: Guia](../tutorial/storage-s3.md)

</div>

## GCP

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-google: __Google Cloud Storage__

    ---

    Persistência em buckets **GCS**.

    [:octicons-arrow-right-24: Guia](../tutorial/storage-gcs.md)

</div>

## Telegram

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-telegram: __Telegram Bot API__

    ---

    Envio de atualizações do fluxo pelo **Telegram**.

    [:octicons-arrow-right-24: Guia](../tutorial/notify-telegram.md)

</div>

## Integrados

<div class="grid cards dotflow-integration-grid" markdown>

- :material-database-outline: __Armazenamento padrão__

    ---

    Armazenamento em memória para testes e início rápido.

    [:octicons-arrow-right-24: Guia](../tutorial/storage-default.md)

- :material-folder-outline: __Armazenamento em arquivo__

    ---

    Contexto e checkpoints no sistema de arquivos local.

    [:octicons-arrow-right-24: Guia](../tutorial/storage-file.md)

- :material-bell-outline: __Notify padrão__

    ---

    Gancho de notificação com implementação padrão simples.

    [:octicons-arrow-right-24: Guia](../tutorial/notify-default.md)

- :material-text-box-outline: __Log padrão__

    ---

    Log estruturado para tarefas e fluxos.

    [:octicons-arrow-right-24: Guia](../tutorial/log-default.md)

- :material-calendar-blank: __Agendador padrão__

    ---

    Agendamento base para fluxos.

    [:octicons-arrow-right-24: Guia](../tutorial/scheduler-default.md)

- :material-clock-outline: __Cron__

    ---

    Execuções recorrentes com expressões cron.

    [:octicons-arrow-right-24: Guia](../tutorial/scheduler-cron.md)

</div>

## Implementação própria

Para um provedor customizado, veja o [Guia de desenvolvimento](../development/custom-providers.md) e a seção **Referência → Métodos abstratos**.
