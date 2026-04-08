# AWS Lambda

Deploy your dotflow pipeline as a container-based AWS Lambda function.

## Create project

```bash
dotflow init
# Select cloud: lambda
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform lambda
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point that calls your workflow |
| `template.yaml` | SAM template defining the function |
| `samconfig.toml` | Pre-configured deployment settings |

## Prerequisites

- `pip install dotflow[aws]`
- AWS CLI configured (`aws configure`)
- Docker

## Deploy

### Option 1: dotflow deploy

```bash
dotflow deploy --platform lambda --project my_pipeline
```

### Option 2: SAM CLI

```bash
aws ecr create-repository --repository-name my_pipeline --region us-east-1
sam build
sam deploy
```

## Invoke

```bash
# Via dotflow deploy
aws lambda invoke --function-name my_pipeline --region us-east-1 /dev/stdout

# Via SAM
sam remote invoke
```

## View logs

```bash
sam logs --stack-name my_pipeline --tail
```

## Variants

| Platform | Trigger | Deploy method |
|----------|---------|---------------|
| `lambda` | Manual invocation | `dotflow deploy` or `sam deploy` |
| `lambda-scheduled` | EventBridge cron/rate | `dotflow deploy --schedule` or `sam deploy` |
| `lambda-s3-trigger` | S3 file upload | `sam deploy` |
| `lambda-sqs-trigger` | SQS message | `sam deploy` |
| `lambda-api-trigger` | HTTP POST via API Gateway | `sam deploy` |

## Important

- Do not rename `handler.py` or the `handler()` function — the Dockerfile CMD is `handler.handler`
- Do not rename `workflow.py` or the `main()` function — `handler.py` imports it
- The `samconfig.toml` has stack name, region, and ECR repository pre-configured
