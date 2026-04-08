"""Lambda deployment."""

from __future__ import annotations

import contextlib

from rich import print  # type: ignore

from dotflow.cloud.aws.services.cloudwatch import CloudWatch
from dotflow.cloud.aws.services.ecr import ECR
from dotflow.cloud.aws.services.iam import IAM
from dotflow.cloud.core import Deployer
from dotflow.settings import Settings as settings


class LambdaDeployer(Deployer):
    """Deploy dotflow pipelines to AWS Lambda."""

    def __init__(self, region: str = "us-east-1"):
        try:
            import boto3
        except ImportError as err:
            raise SystemExit(
                "boto3 is required: pip install dotflow[aws]"
            ) from err

        self._region = region
        self._lambda = boto3.client("lambda", region_name=region)
        self._events = boto3.client("events", region_name=region)

        sts = boto3.client("sts", region_name=region)
        self._account_id = sts.get_caller_identity()["Account"]

        self._ecr = ECR(
            boto3.client("ecr", region_name=region),
            self._account_id,
            region,
        )
        self._iam = IAM(boto3.client("iam", region_name=region))
        self._logs = CloudWatch(boto3.client("logs", region_name=region))

    def setup(self, name: str) -> None:
        """Create IAM role and CloudWatch log group."""
        self._role_arn = self._iam.ensure_lambda_role(name)
        self._logs.ensure_log_group(f"/aws/lambda/{name}")

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy a Lambda function from the current directory."""
        schedule = kwargs.get("schedule")

        print(settings.INFO_ALERT, f"Deploying Lambda '{name}'...")

        self.setup(name)
        image_uri = self._ecr.push(name)
        self._create_or_update(name, image_uri, self._role_arn)

        if schedule:
            self._create_schedule(name, schedule)

        print(settings.INFO_ALERT, "Done.")

    def _create_or_update(self, name: str, image_uri: str, role_arn: str):
        """Create or update Lambda function."""
        try:
            self._lambda.get_function(FunctionName=name)
            print("  Updating Lambda function...")
            self._lambda.update_function_code(
                FunctionName=name,
                ImageUri=image_uri,
            )
        except self._lambda.exceptions.ResourceNotFoundException:
            print("  Creating Lambda function...")
            self._lambda.create_function(
                FunctionName=name,
                PackageType="Image",
                Code={"ImageUri": image_uri},
                Role=role_arn,
                Timeout=900,
                MemorySize=512,
            )

    def _create_schedule(self, name: str, schedule: str):
        """Create EventBridge schedule rule for Lambda."""
        rule_name = f"{name}-schedule"
        function_arn = (
            f"arn:aws:lambda:{self._region}:{self._account_id}:function:{name}"
        )

        print(f"  Creating EventBridge rule '{rule_name}'...")
        self._events.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule,
            State="ENABLED",
        )

        with contextlib.suppress(
            self._lambda.exceptions.ResourceConflictException
        ):
            self._lambda.add_permission(
                FunctionName=name,
                StatementId=rule_name,
                Action="lambda:InvokeFunction",
                Principal="events.amazonaws.com",
                SourceArn=(
                    f"arn:aws:events:{self._region}:{self._account_id}"
                    f":rule/{rule_name}"
                ),
            )

        self._events.put_targets(
            Rule=rule_name,
            Targets=[{"Id": "1", "Arn": function_arn}],
        )

        print(f"  Schedule: {schedule}")
