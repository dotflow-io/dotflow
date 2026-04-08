# Cloud Deployment

Deploy your dotflow pipelines to any major cloud provider. Choose a target platform during project creation and get all the infrastructure files you need — fully configured and ready to deploy.

## Quick start

```bash
# 1. Create a new project with cloud support
dotflow init

# 2. Enter the project
cd my_pipeline

# 3. Deploy
dotflow deploy --platform lambda --project my_pipeline
```

## CLI

| Command | Description |
|---------|-------------|
| `dotflow init` | Scaffold a new project (select cloud platform during setup) |
| `dotflow cloud list` | Show available deployment platforms |
| `dotflow cloud generate --platform <name>` | Generate deployment files for an existing project |
| `dotflow deploy --platform <name> --project <name>` | Deploy to a cloud platform |

### Deploy options

```bash
dotflow deploy --platform <name> --project <name> [--region <region>] [--schedule <expression>]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--platform` | required | Target platform (`lambda`, `lambda-scheduled`, `ecs`) |
| `--project` | required | Project name |
| `--region` | `us-east-1` | AWS region |
| `--schedule` | — | Schedule expression (e.g. `rate(6 hours)`) |

### Deploy examples

```bash
# AWS Lambda
dotflow deploy --platform lambda --project my_pipeline

# AWS Lambda with schedule
dotflow deploy --platform lambda-scheduled --project my_pipeline --schedule "rate(6 hours)"

# AWS ECS Fargate
dotflow deploy --platform ecs --project my_pipeline --region us-east-1

# Docker (no deploy command needed)
docker compose build && docker compose up

# Kubernetes
kubectl apply -f deployment.yaml -f service.yaml

# GCP Cloud Run
gcloud run deploy my_pipeline --source . --region us-central1

# Platforms with triggers (S3, SQS, API Gateway, ECS scheduled)
sam build && sam deploy
```

### Supported platforms

| Platform | `dotflow deploy` | `sam deploy` | Manual |
|----------|:---:|:---:|:---:|
| `lambda` | :white_check_mark: | :white_check_mark: | — |
| `lambda-scheduled` | :white_check_mark: | :white_check_mark: | — |
| `lambda-s3-trigger` | — | :white_check_mark: | — |
| `lambda-sqs-trigger` | — | :white_check_mark: | — |
| `lambda-api-trigger` | — | :white_check_mark: | — |
| `ecs` | :white_check_mark: | — | — |
| `ecs-scheduled` | — | — | CloudFormation |
| `cloud-run` | — | — | `gcloud` |
| `cloud-run-scheduled` | — | — | `gcloud` |
| `docker` | — | — | `docker compose` |
| `kubernetes` | — | — | `kubectl` |

## Docker

<div class="grid cards" markdown>

- :fontawesome-brands-docker: **Docker**

    ---

    `Dockerfile` + `docker-compose.yml` for local or any container runtime.

    [:octicons-arrow-right-24: Guide](docker.md)

</div>

## AWS

<div class="grid cards" markdown>

- :fontawesome-brands-aws: **Lambda**

    ---

    Container-based Lambda function. Deploy with `dotflow deploy` or `sam deploy`.

    [:octicons-arrow-right-24: Guide](lambda.md)

- :fontawesome-brands-aws: **Lambda + EventBridge**

    ---

    Scheduled Lambda with cron/rate expressions. Deploy with `dotflow deploy --schedule`.

    [:octicons-arrow-right-24: Guide](lambda-scheduled.md)

- :fontawesome-brands-aws: **Lambda + S3 Trigger**

    ---

    Pipeline triggered by S3 file upload. Deploy with `sam deploy`.

    [:octicons-arrow-right-24: Guide](lambda-s3-trigger.md)

- :fontawesome-brands-aws: **Lambda + SQS Trigger**

    ---

    Pipeline triggered by SQS messages. Deploy with `sam deploy`.

    [:octicons-arrow-right-24: Guide](lambda-sqs-trigger.md)

- :fontawesome-brands-aws: **Lambda + API Gateway**

    ---

    Pipeline triggered by HTTP POST. Deploy with `sam deploy`.

    [:octicons-arrow-right-24: Guide](lambda-api-trigger.md)

- :fontawesome-brands-aws: **ECS Fargate**

    ---

    Task definition for ECS Fargate. Deploy with `dotflow deploy`.

    [:octicons-arrow-right-24: Guide](ecs.md)

- :fontawesome-brands-aws: **ECS + EventBridge**

    ---

    Scheduled Fargate task. Deploy with CloudFormation.

    [:octicons-arrow-right-24: Guide](ecs-scheduled.md)

</div>

## GCP

<div class="grid cards" markdown>

- :fontawesome-brands-google: **Cloud Run**

    ---

    Deploy with `gcloud run deploy`.

    [:octicons-arrow-right-24: Guide](cloud-run.md)

- :fontawesome-brands-google: **Cloud Run + Scheduler**

    ---

    Scheduled Cloud Run with Cloud Scheduler.

    [:octicons-arrow-right-24: Guide](cloud-run-scheduled.md)

</div>

## Kubernetes

<div class="grid cards" markdown>

- :material-kubernetes: **Kubernetes**

    ---

    Deploy with `kubectl apply`.

    [:octicons-arrow-right-24: Guide](kubernetes.md)

</div>

## Azure :soon:

<div class="grid cards" markdown>

- :material-microsoft-azure: **Azure Functions**

    ---

    Timer-triggered function with `function.json`.

- :material-microsoft-azure: **Azure Container Apps**

    ---

    Containerized pipeline on Azure Container Apps.

</div>

## Coming soon :soon:

<div class="grid cards" markdown>

- :material-cloud-outline: **Heroku**

    ---

    `Procfile` + `heroku.yml` for Heroku deployment.

- :simple-flydotio: **Fly.io**

    ---

    `fly.toml` for Fly.io edge deployment.

- :simple-railway: **Railway**

    ---

    `railway.json` for Railway deployment.

- :simple-render: **Render**

    ---

    `render.yaml` for Render deployment.

- :simple-digitalocean: **DigitalOcean**

    ---

    `app.yaml` for DigitalOcean App Platform.

</div>
