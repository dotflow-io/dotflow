"""GCP constants."""

GCP_SDK_NOT_FOUND = (
    "google-cloud-run is required: pip install dotflow[deploy-gcp]"
)

CREDENTIALS_NOT_FOUND = (
    "GCP credentials not found. "
    "Run 'gcloud auth application-default login' "
    "or set GOOGLE_APPLICATION_CREDENTIALS environment variable."
)
