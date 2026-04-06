# Storage S3

Persists task output to AWS S3. Good for serverless and cloud-native workflows.

/// note
Requires `pip install dotflow[aws]`
///

## Example

{* ./docs_src/storage/storage_s3.py ln[1:28] hl[2,16:22] *}

## Authentication

`StorageS3` uses the default boto3 credential chain:

1. Environment variables: `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
2. Shared credentials file: `~/.aws/credentials`
3. IAM Role: automatic on Lambda, EC2, ECS

No credentials are needed in code — boto3 handles it transparently.

## References

- [StorageS3](https://dotflow-io.github.io/dotflow/nav/reference/storage-s3/)
