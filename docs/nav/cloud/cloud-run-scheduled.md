# Google Cloud Run + Cloud Scheduler

Run your dotflow pipeline on a recurring schedule using Cloud Run and Cloud Scheduler.

## Create project

```bash
dotflow init
# Select cloud: cloud-run-scheduled
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform cloud-run-scheduled
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `cloudbuild.yaml` | Cloud Build configuration |
| `scheduler.yaml` | Cloud Scheduler job definition |

## Prerequisites

- Google Cloud CLI (`gcloud`) installed and authenticated

## Deploy

```bash
gcloud auth login
gcloud config set project <gcp_project_id>

gcloud services enable cloudbuild.googleapis.com run.googleapis.com cloudscheduler.googleapis.com

gcloud run deploy my_pipeline --source . --region us-central1 --no-allow-unauthenticated

gcloud scheduler jobs create http my_pipeline-trigger \
  --schedule="0 */6 * * *" \
  --uri="<cloud_run_url>" \
  --http-method=POST \
  --oidc-service-account-email=<project_number>-compute@developer.gserviceaccount.com \
  --location=us-central1
```

## Important

- Replace `<cloud_run_url>` with the actual URL from the `gcloud run deploy` output
- The scheduler uses OIDC authentication to invoke the Cloud Run service
