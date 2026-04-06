# Storage GCS

Persists task output to Google Cloud Storage. Good for serverless and cloud-native workflows on GCP.

/// note
Requires `pip install dotflow[gcp]`
///

## Example

{* ./docs_src/storage/storage_gcs.py ln[1:34] hl[2,16:22] *}

## Authentication

`StorageGCS` uses Application Default Credentials (ADC):

1. Environment variable: `GOOGLE_APPLICATION_CREDENTIALS` pointing to a service account JSON
2. `gcloud auth application-default login` for local development
3. Service account: automatic on Cloud Run, Cloud Functions, GKE

No credentials are needed in code — the GCP client handles it transparently.

## References

- [StorageGCS](https://dotflow-io.github.io/dotflow/nav/reference/storage-gcs/)
