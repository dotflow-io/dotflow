# Install

To install **Dotflow**, run the following command from the command line:

## With Pip

```bash
pip install dotflow
```

##  With Poetry

```bash
poetry add dotflow
```

## Optional dependencies

Dotflow has optional extras for specific providers:

| Extra | Command | What it enables |
|-------|---------|-----------------|
| `aws` | `pip install dotflow[aws]` | StorageS3 — AWS S3 persistence |
| `gcp` | `pip install dotflow[gcp]` | StorageGCS — Google Cloud Storage persistence |
| `scheduler` | `pip install dotflow[scheduler]` | SchedulerCron — cron-based recurring execution |
| `otel` | `pip install dotflow[otel]` | LogOpenTelemetry — OpenTelemetry traces and spans |

Multiple extras can be installed at once:

```bash
pip install dotflow[aws,scheduler]
```
