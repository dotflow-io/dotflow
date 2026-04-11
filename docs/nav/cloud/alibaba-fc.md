# Alibaba Cloud Function Compute

Deploy your dotflow pipeline to Alibaba Cloud Function Compute (FC).

## Create project

```bash
dotflow init
# Select cloud: alibaba-fc
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform alibaba-fc
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `handler.py` | FC entry point that calls your workflow |
| `s.yaml` | Serverless Devs template |

## Prerequisites

- `pip install dotflow[deploy-alibaba]`
- Alibaba Cloud CLI configured (`aliyun configure`)
- Docker
- Container Registry namespace created
- `ALIBABA_CR_PASSWORD` env var set

## Deploy

```bash
dotflow deploy --platform alibaba-fc --project my-pipeline
```

## Variants

| Platform | Trigger | Deploy method |
|----------|---------|---------------|
| `alibaba-fc` | Manual invocation | `dotflow deploy` |
| `alibaba-fc-scheduled` | Timer trigger (cron) | `dotflow deploy --schedule` |
