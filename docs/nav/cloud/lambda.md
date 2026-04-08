# AWS Lambda

Deploy your dotflow pipeline as a container-based AWS Lambda function using SAM.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point that calls your workflow |
| `template.yaml` | SAM template defining the function |
| `samconfig.toml` | Pre-configured deployment settings |

## Prerequisites

- AWS CLI configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (`brew install aws-sam-cli`)
- Docker

## Deploy

```bash
# Create ECR repository (first time only)
aws ecr create-repository --repository-name <project_name> --region us-east-1

sam build
sam deploy
```

## Invoke

```bash
sam remote invoke
```

## View logs

```bash
sam logs --stack-name <project_name> --tail
```

## Variants

| Platform | Trigger |
|----------|---------|
| `lambda` | Manual invocation |
| `lambda-scheduled` | EventBridge cron/rate schedule |
| `lambda-s3-trigger` | S3 file upload |
| `lambda-sqs-trigger` | SQS message |
| `lambda-api-trigger` | HTTP POST via API Gateway |

All variants use the same deploy flow: `sam build && sam deploy`.

## Important

- Do not rename `handler.py` or the `handler()` function — the Dockerfile CMD is `handler.handler`
- Do not rename `workflow.py` or the `main()` function — `handler.py` imports it
- The `samconfig.toml` has stack name, region, and ECR repository pre-configured
