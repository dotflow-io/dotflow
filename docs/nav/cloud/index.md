# Cloud Deployment

Deploy your dotflow pipelines to any major cloud provider. Choose a target platform during project creation and get all the infrastructure files you need — fully configured and ready to deploy.

## Getting started

```bash
pip install dotflow
dotflow init
```

Select a cloud platform during setup. The generated project includes Dockerfiles, deployment manifests, and configuration files for your chosen platform.

## CLI

| Command | Description |
|---------|-------------|
| `dotflow cloud list` | Show available deployment platforms |
| `dotflow cloud generate --platform <name>` | Generate deployment files for your project |

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

    Container-based Lambda function with SAM.

    [:octicons-arrow-right-24: Guide](lambda.md)

- :fontawesome-brands-aws: **Lambda + EventBridge**

    ---

    Scheduled Lambda with cron/rate expressions.

    [:octicons-arrow-right-24: Guide](lambda-scheduled.md)

- :fontawesome-brands-aws: **Lambda + S3 Trigger**

    ---

    Pipeline triggered by S3 file upload.

    [:octicons-arrow-right-24: Guide](lambda-s3-trigger.md)

- :fontawesome-brands-aws: **Lambda + SQS Trigger**

    ---

    Pipeline triggered by SQS messages.

    [:octicons-arrow-right-24: Guide](lambda-sqs-trigger.md)

- :fontawesome-brands-aws: **Lambda + API Gateway**

    ---

    Pipeline triggered by HTTP POST.

    [:octicons-arrow-right-24: Guide](lambda-api-trigger.md)

- :fontawesome-brands-aws: **ECS Fargate**

    ---

    Task definition for ECS Fargate.

    [:octicons-arrow-right-24: Guide](ecs.md)

- :fontawesome-brands-aws: **ECS + EventBridge**

    ---

    Scheduled Fargate task with EventBridge.

    [:octicons-arrow-right-24: Guide](ecs-scheduled.md)

</div>

## GCP

<div class="grid cards" markdown>

- :fontawesome-brands-google: **Cloud Run**

    ---

    Deploy with `cloudbuild.yaml` to Cloud Run.

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

    Deployment + service manifests for any cluster.

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
