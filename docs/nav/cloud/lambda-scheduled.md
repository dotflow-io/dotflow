# AWS Lambda + EventBridge Schedule

Run your dotflow pipeline on a recurring schedule using AWS Lambda and EventBridge.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point |
| `template.yaml` | SAM template with EventBridge schedule trigger |
| `samconfig.toml` | Pre-configured deployment settings |

## Deploy

```bash
aws ecr create-repository --repository-name <project_name> --region us-east-1

sam build
sam deploy
```

## View logs

```bash
sam logs --stack-name <project_name> --tail
```

## Important

- The schedule expression is configured during project creation (e.g. `rate(6 hours)`, `cron(0 12 * * ? *)`)
- Edit `template.yaml` to change the schedule after generation
