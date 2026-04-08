# Google Cloud Run + Cloud Scheduler

Run your dotflow pipeline on a recurring schedule using Cloud Run and Cloud Scheduler.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `cloudbuild.yaml` | Cloud Build configuration |
| `scheduler.yaml` | Cloud Scheduler job definition |

## Deploy

```bash
gcloud auth login
gcloud config set project <gcp_project_id>

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com cloudscheduler.googleapis.com

# Deploy Cloud Run service
gcloud run deploy <project_name> --source . --region us-central1 --no-allow-unauthenticated

# Create Cloud Scheduler job (use the URL from deploy output)
gcloud scheduler jobs create http <project_name>-trigger \
  --schedule="0 */6 * * *" \
  --uri="<cloud_run_url>" \
  --http-method=POST \
  --oidc-service-account-email=<project_number>-compute@developer.gserviceaccount.com \
  --location=us-central1
```

## Important

- Replace `<cloud_run_url>` with the actual URL from the `gcloud run deploy` output
- The scheduler uses OIDC authentication to invoke the Cloud Run service
- Edit `scheduler.yaml` to change the cron schedule
