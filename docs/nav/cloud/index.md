# Cloud Deployment

Deploy your dotflow pipelines to any major cloud provider. Choose a target platform during project creation and get all the infrastructure files you need — fully configured and ready to deploy.

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

- :fontawesome-brands-aws: **Step Functions** :soon:

    ---

    State machine with Lambda tasks via SAM.

    [:octicons-arrow-right-24: Guide](step-functions.md)

- :fontawesome-brands-aws: **Batch** :soon:

    ---

    Fargate batch job for heavy workloads.

    [:octicons-arrow-right-24: Guide](aws-batch.md)

- :fontawesome-brands-aws: **App Runner** :soon:

    ---

    Serverless container service with minimal config.

    [:octicons-arrow-right-24: Guide](app-runner.md)

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

- :fontawesome-brands-google: **Cloud Functions** :soon:

    ---

    Serverless function with HTTP trigger.

    [:octicons-arrow-right-24: Guide](cloud-functions.md)

- :fontawesome-brands-google: **Cloud Workflows** :soon:

    ---

    Orchestration workflow definition.

    [:octicons-arrow-right-24: Guide](cloud-workflows.md)

- :fontawesome-brands-google: **Cloud Tasks** :soon:

    ---

    HTTP task queue with Cloud Run backend.

    [:octicons-arrow-right-24: Guide](cloud-tasks.md)

- :fontawesome-brands-google: **Pub/Sub Trigger** :soon:

    ---

    Cloud Run triggered by Pub/Sub messages.

    [:octicons-arrow-right-24: Guide](pubsub-trigger.md)

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

    [:octicons-arrow-right-24: Guide](azure-functions.md)

- :material-microsoft-azure: **Azure Container Apps**

    ---

    Containerized pipeline on Azure Container Apps.

    [:octicons-arrow-right-24: Guide](azure-container.md)

- :material-microsoft-azure: **Azure Container Instances** :soon:

    ---

    One-shot container execution.

    [:octicons-arrow-right-24: Guide](azure-container-instances.md)

- :material-microsoft-azure: **Azure Logic Apps** :soon:

    ---

    Orchestration workflow with HTTP trigger.

    [:octicons-arrow-right-24: Guide](azure-logic-apps.md)

- :material-microsoft-azure: **Azure Queue Trigger** :soon:

    ---

    Azure Function triggered by Storage Queue messages.

    [:octicons-arrow-right-24: Guide](azure-queue-trigger.md)

</div>

## CI/CD

<div class="grid cards" markdown>

- :fontawesome-brands-github: **GitHub Actions**

    ---

    Scheduled workflow running on GitHub Actions runner.

    [:octicons-arrow-right-24: Guide](github-actions.md)

- :fontawesome-brands-gitlab: **GitLab CI** :soon:

    ---

    CI/CD pipeline with schedule and manual trigger.

    [:octicons-arrow-right-24: Guide](gitlab-ci.md)

</div>

## More platforms :soon:

<div class="grid cards" markdown>

- :material-cloud-outline: **Heroku**

    ---

    `Procfile` + `heroku.yml` for Heroku deployment.

    [:octicons-arrow-right-24: Guide](heroku.md)

- :material-cloud-outline: **Fly.io**

    ---

    `fly.toml` for Fly.io edge deployment.

    [:octicons-arrow-right-24: Guide](fly-io.md)

- :material-cloud-outline: **Railway**

    ---

    `railway.json` for Railway deployment.

    [:octicons-arrow-right-24: Guide](railway.md)

- :material-cloud-outline: **Render**

    ---

    `render.yaml` for Render deployment.

    [:octicons-arrow-right-24: Guide](render.md)

- :material-cloud-outline: **DigitalOcean**

    ---

    `app.yaml` for DigitalOcean App Platform.

    [:octicons-arrow-right-24: Guide](digital-ocean.md)

- :material-cloud-outline: **Vercel** :soon:

    ---

    Serverless function via HTTP endpoint.

    [:octicons-arrow-right-24: Guide](vercel.md)

- :material-cloud-outline: **Coolify** :soon:

    ---

    Self-hosted PaaS deployment via Docker.

    [:octicons-arrow-right-24: Guide](coolify.md)

- :material-cloud-outline: **Nomad** :soon:

    ---

    Batch job for HashiCorp Nomad orchestrator.

    [:octicons-arrow-right-24: Guide](nomad.md)

- :material-cloud-outline: **Terraform** :soon:

    ---

    Infrastructure as Code.

    [:octicons-arrow-right-24: Guide](terraform.md)

</div>
