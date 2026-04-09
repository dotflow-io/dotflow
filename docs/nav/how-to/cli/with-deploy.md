# With Deploy

Deploy a dotflow pipeline to a cloud platform.

## AWS Lambda

```bash
dotflow deploy --platform lambda --project my-pipeline
```

## AWS Lambda Scheduled

```bash
dotflow deploy --platform lambda-scheduled --project my-pipeline --schedule "*/5 * * * *"
```

If `--schedule` is not provided, dotflow reads from `template.yaml` or prompts for a cron expression.

## AWS Lambda + S3 Trigger

```bash
dotflow deploy --platform lambda-s3-trigger --project my-pipeline
```

## AWS Lambda + SQS Trigger

```bash
dotflow deploy --platform lambda-sqs-trigger --project my-pipeline
```

## AWS Lambda + API Gateway

```bash
dotflow deploy --platform lambda-api-trigger --project my-pipeline
```

## AWS ECS Fargate

```bash
dotflow deploy --platform ecs --project my-pipeline
```

## AWS ECS Scheduled

```bash
dotflow deploy --platform ecs-scheduled --project my-pipeline --schedule "0 */6 * * *"
```

## Google Cloud Run

```bash
dotflow deploy --platform cloud-run --project my-pipeline
```

## GitHub Actions

```bash
dotflow deploy --platform github-actions --project my-pipeline
```

## Options

| Option | Description |
|--------|-------------|
| `--platform` | Target platform (required) |
| `--project` | Project name (required) |
| `--region` | Cloud region (default: us-east-1 for AWS, us-central1 for GCP) |
| `--schedule` | Cron expression for scheduled platforms (e.g. `*/5 * * * *`) |

!!! note
    Cron expressions use standard 5-field format (`min hour day month weekday`). Dotflow converts to the cloud provider format automatically (e.g. AWS EventBridge `cron()`).

!!! note
    AWS deploy requires `pip install dotflow[deploy-aws]`. GCP deploy requires `pip install dotflow[deploy-gcp]`. GitHub Actions requires `pip install dotflow[deploy-github]`.
