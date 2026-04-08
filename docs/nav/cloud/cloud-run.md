# Google Cloud Run

Deploy your dotflow pipeline to Google Cloud Run.

## Create project

```bash
dotflow init
# Select cloud: cloud-run
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform cloud-run
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `cloudbuild.yaml` | Cloud Build configuration |

## Prerequisites

- Google Cloud CLI (`gcloud`) installed and authenticated

## Deploy

```bash
gcloud auth login
gcloud config set project <gcp_project_id>

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com

# Deploy (builds and deploys in one step)
gcloud run deploy my_pipeline --source . --region us-central1 --no-allow-unauthenticated
```

## View logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=my_pipeline" --limit 50 --format="value(textPayload)"
```

## Important

- Do not rename `workflow.py` or the `main()` function — the Dockerfile CMD depends on it
- Enable all required APIs before deploying
