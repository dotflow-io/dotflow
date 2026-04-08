# AWS Lambda + API Gateway

Trigger your dotflow pipeline via HTTP POST through API Gateway.

## Create project

```bash
dotflow init
# Select cloud: lambda-api-trigger
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform lambda-api-trigger
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point with JSON body parsing |
| `template.yaml` | SAM template with HTTP API event |
| `samconfig.toml` | Pre-configured deployment settings |

## Prerequisites

- `pip install dotflow[deploy-aws]`
- AWS CLI configured (`aws configure`)
- Docker

## Deploy

### Option 1: dotflow deploy

```bash
dotflow deploy --platform lambda-api-trigger --project my_pipeline
```

The endpoint URL is shown after deploy.

### Option 2: SAM CLI

```bash
aws ecr create-repository --repository-name my_pipeline --region us-east-1
sam build
sam deploy
```

## Invoke

```bash
curl -X POST https://<api_id>.execute-api.us-east-1.amazonaws.com/workflow
```

## View logs

```bash
aws logs tail /aws/lambda/my_pipeline --region us-east-1 --since 5m
```

## Important

- The endpoint accepts POST requests at `/workflow`
- The request body is parsed as JSON and available in `handler.py`
