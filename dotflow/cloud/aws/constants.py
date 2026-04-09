"""AWS constants."""

CREDENTIALS_NOT_FOUND = (
    "AWS credentials not found. "
    "Run 'aws configure' or set AWS_ACCESS_KEY_ID "
    "and AWS_SECRET_ACCESS_KEY environment variables."
)

BOTO3_NOT_FOUND = "boto3 is required: pip install dotflow[deploy-aws]"

PLATFORMS = {
    "lambda",
    "lambda-scheduled",
    "lambda-s3-trigger",
    "lambda-sqs-trigger",
    "lambda-api-trigger",
    "ecs",
    "ecs-scheduled",
}

SCHEDULED_PLATFORMS = {"lambda-scheduled", "ecs-scheduled"}

DEFAULT_REGION = "us-east-1"
