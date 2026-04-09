"""Lambda + S3 Trigger deployment."""

from __future__ import annotations

import contextlib

from rich import print  # type: ignore

from dotflow.cloud.aws.deployers.base_lambda_deployer import BaseLambdaDeployer
from dotflow.settings import Settings as settings


class LambdaS3Deployer(BaseLambdaDeployer):
    """Deploy dotflow pipeline as Lambda + S3 Trigger."""

    def _configure_trigger(self, name: str, **kwargs) -> None:
        """Create S3 bucket with Lambda notification."""
        s3 = self._boto3.client("s3", region_name=self._region)
        bucket_name = f"{name}-source"

        print(f"  {settings.STEP_ICON} Creating S3 bucket '{bucket_name}'...")
        try:
            if self._region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        "LocationConstraint": self._region
                    },
                )
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass

        with contextlib.suppress(
            self._lambda.exceptions.ResourceConflictException
        ):
            self._lambda.add_permission(
                FunctionName=name,
                StatementId=f"{name}-s3-invoke",
                Action="lambda:InvokeFunction",
                Principal="s3.amazonaws.com",
                SourceArn=f"arn:aws:s3:::{bucket_name}",
            )

        print(f"  {settings.STEP_ICON} Configuring S3 notification...")
        s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                "LambdaFunctionConfigurations": [
                    {
                        "LambdaFunctionArn": self._function_arn,
                        "Events": ["s3:ObjectCreated:*"],
                    }
                ]
            },
        )

        print(f"  {settings.STEP_ICON} Trigger: s3://{bucket_name}/*")
