# AWS Lambda + EventBridge Schedule

Run your dotflow pipeline on a recurring schedule using AWS Lambda and EventBridge.

## Create project

```bash
dotflow init
# Select cloud: lambda-scheduled
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform lambda-scheduled
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point |
| `template.yaml` | SAM template with EventBridge schedule trigger |
| `samconfig.toml` | Pre-configured deployment settings |

## Prerequisites

- `pip install dotflow[aws]`
- AWS CLI configured (`aws configure`)
- Docker

## Deploy

### Option 1: dotflow deploy

```bash
dotflow deploy --platform lambda-scheduled --project my_pipeline --schedule "0 */6 * * *"
```

### Option 2: SAM CLI

```bash
aws ecr create-repository --repository-name my_pipeline --region us-east-1
sam build
sam deploy
```

## View logs

```bash
sam logs --stack-name my_pipeline --tail
```

## Important

- Use standard cron format (e.g. `0 */6 * * *`). Dotflow converts to AWS EventBridge format automatically
- Edit `template.yaml` to change the schedule after generation
