# AWS Lambda + SQS Trigger

Run your dotflow pipeline when a message arrives in an SQS queue.

## Create project

```bash
dotflow init
# Select cloud: lambda-sqs-trigger
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform lambda-sqs-trigger
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point |
| `template.yaml` | SAM template with SQS event source |
| `samconfig.toml` | Pre-configured deployment settings |

## Prerequisites

- AWS CLI configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (`brew install aws-sam-cli`)
- Docker

## Deploy

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

- The SAM template creates an SQS queue named `<project_name>-queue`
- Messages are processed one at a time (`BatchSize: 1`)
- `VisibilityTimeout` is set to 960s (Lambda timeout + buffer)
