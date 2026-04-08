# AWS Lambda + S3 Trigger

Run your dotflow pipeline automatically when a file is uploaded to an S3 bucket.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Lambda container image |
| `handler.py` | Lambda entry point |
| `template.yaml` | SAM template with S3 event trigger |
| `samconfig.toml` | Pre-configured deployment settings |

## Deploy

```bash
aws ecr create-repository --repository-name <project_name> --region us-east-1

sam build
sam deploy
```

## Important

- The SAM template creates an S3 bucket named `<project_name>-source`
- The pipeline triggers on any file upload (`s3:ObjectCreated:*`)
- Edit `template.yaml` to filter by prefix or suffix
