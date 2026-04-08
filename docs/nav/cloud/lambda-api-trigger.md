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

- AWS CLI configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (`brew install aws-sam-cli`)
- Docker

## Deploy

```bash
aws ecr create-repository --repository-name my_pipeline --region us-east-1
sam build
sam deploy
```

The API Gateway URL is shown in the CloudFormation outputs after deploy.

## Invoke

```bash
curl -X POST https://<api_id>.execute-api.us-east-1.amazonaws.com/workflow
```

## View logs

```bash
sam logs --stack-name my_pipeline --tail
```

## Important

- The endpoint accepts POST requests at `/workflow`
- The request body is parsed as JSON and available in `handler.py`
