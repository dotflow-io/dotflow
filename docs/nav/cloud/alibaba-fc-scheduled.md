# Alibaba Cloud FC Scheduled

Deploy your dotflow pipeline to Alibaba Cloud Function Compute with a timer trigger.

## Create project

```bash
dotflow init
# Select cloud: alibaba-fc-scheduled
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform alibaba-fc-scheduled
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `handler.py` | FC entry point that calls your workflow |
| `s.yaml` | Serverless Devs template with timer trigger |

## Prerequisites

- `pip install dotflow[deploy-alibaba]`
- Alibaba Cloud CLI configured (`aliyun configure`)
- Docker
- Container Registry namespace created
- `ALIBABA_CR_PASSWORD` env var set

## Deploy

```bash
dotflow deploy --platform alibaba-fc-scheduled --project my-pipeline --schedule "0 */6 * * *"
```

If `--schedule` is not provided, dotflow prompts for a cron expression.

## Cron format

Standard 5-field crontab: `min hour day month weekday`

| Expression | Meaning |
|------------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 */6 * * *` | Every 6 hours |
| `0 0 * * *` | Daily at midnight |
| `0 6 * * 1` | Every Monday at 6am |
