# AWS Lambda + SQS Trigger

Run your dotflow pipeline when a message arrives in an SQS queue.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point |
| `template.yaml` | SAM template with SQS event source |
| `samconfig.toml` | Pre-configured deployment settings |

## Deploy

```bash
aws ecr create-repository --repository-name <project_name> --region us-east-1

sam build
sam deploy
```

## Important

- The SAM template creates an SQS queue named `<project_name>-queue`
- Messages are processed one at a time (`BatchSize: 1`)
- `VisibilityTimeout` is set to 960s (Lambda timeout + buffer)
