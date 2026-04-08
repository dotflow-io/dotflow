# AWS Lambda + API Gateway

Trigger your dotflow pipeline via HTTP POST through API Gateway.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point with JSON body parsing |
| `template.yaml` | SAM template with HTTP API event |
| `samconfig.toml` | Pre-configured deployment settings |

## Deploy

```bash
aws ecr create-repository --repository-name <project_name> --region us-east-1

sam build
sam deploy
```

The API Gateway URL is shown in the CloudFormation outputs after deploy.

## Invoke

```bash
curl -X POST https://<api_id>.execute-api.us-east-1.amazonaws.com/workflow
```

## Important

- The endpoint accepts POST requests at `/workflow`
- The request body is parsed as JSON and available in `handler.py`
