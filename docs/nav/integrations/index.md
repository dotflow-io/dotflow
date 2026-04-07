# Overview

## AWS

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-aws: __Amazon S3__

    ---

    Durable workflow state in **AWS S3** for cloud and serverless setups.

    [:octicons-arrow-right-24: How-to](../tutorial/storage-s3.md)

</div>

## GCP

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-google: __Google Cloud Storage__

    ---

    Persist output and checkpoints in **GCS** buckets.

    [:octicons-arrow-right-24: How-to](../tutorial/storage-gcs.md)

</div>

## Telegram

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-telegram: __Telegram Bot API__

    ---

    Send workflow updates through **Telegram**.

    [:octicons-arrow-right-24: How-to](../tutorial/notify-telegram.md)

</div>

## Discord

<div class="grid cards dotflow-integration-grid" markdown>

- :fontawesome-brands-discord: __Discord Webhook__

    ---

    Send workflow updates through **Discord** channels.

    [:octicons-arrow-right-24: How-to](../tutorial/notify-discord.md)

</div>

## OpenTelemetry

<div class="grid cards dotflow-integration-grid" markdown>

- :material-chart-timeline-variant: __Traces__

    ---

    Export **distributed traces** with spans per workflow and task to Jaeger, Grafana Tempo, Datadog, or any OTLP-compatible backend.

    [:octicons-arrow-right-24: How-to](../tutorial/tracer-opentelemetry.md)

- :material-chart-bar: __Metrics__

    ---

    Export **counters and histograms** for workflow throughput, task duration, retries, and failures.

    [:octicons-arrow-right-24: How-to](../tutorial/metrics-opentelemetry.md)

</div>

## Built-in

<div class="grid cards dotflow-integration-grid" markdown>

- :material-database-outline: __Default storage__

    ---

    In-memory storage for quick starts and tests.

    [:octicons-arrow-right-24: How-to](../tutorial/storage-default.md)

- :material-folder-outline: __File storage__

    ---

    Local filesystem context and checkpoints.

    [:octicons-arrow-right-24: How-to](../tutorial/storage-file.md)

- :material-bell-outline: __Default notify__

    ---

    Pluggable notification hook with a simple default.

    [:octicons-arrow-right-24: How-to](../tutorial/notify-default.md)

- :material-text-box-outline: __Default log__

    ---

    Structured logging for tasks and workflows.

    [:octicons-arrow-right-24: How-to](../tutorial/log-default.md)

- :material-calendar-blank: __Default scheduler__

    ---

    Baseline scheduling for workflows.

    [:octicons-arrow-right-24: How-to](../tutorial/scheduler-default.md)

- :material-clock-outline: __Cron__

    ---

    Recurring runs with cron expressions.

    [:octicons-arrow-right-24: How-to](../tutorial/scheduler-cron.md)

</div>

## Build your own

To implement a custom provider, see the [Development Guide](../development/custom-providers.md) and the **Reference → Abstract methods** section.
