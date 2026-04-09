"""Base Lambda deployment — shared logic for all Lambda variants."""

from __future__ import annotations

from rich import print  # type: ignore

from dotflow.cloud.aws.constants import BOTO3_NOT_FOUND, CREDENTIALS_NOT_FOUND
from dotflow.cloud.aws.services.cloudwatch import CloudWatch
from dotflow.cloud.aws.services.ecr import ECR
from dotflow.cloud.aws.services.iam import IAM
from dotflow.cloud.core import Deployer
from dotflow.settings import Settings as settings


class BaseLambdaDeployer(Deployer):
    """Shared logic for all Lambda deployers."""

    def __init__(self, region: str = "us-east-1"):
        try:
            import boto3
        except ImportError as err:
            raise SystemExit(BOTO3_NOT_FOUND) from err

        try:
            sts = boto3.client("sts", region_name=region)
            self._account_id = sts.get_caller_identity()["Account"]
        except Exception as err:
            raise SystemExit(CREDENTIALS_NOT_FOUND) from err

        self._region = region
        self._boto3 = boto3
        self._lambda = boto3.client("lambda", region_name=region)

        self._ecr = ECR(
            boto3.client("ecr", region_name=region),
            self._account_id,
            region,
        )
        self._iam = IAM(boto3.client("iam", region_name=region))
        self._logs = CloudWatch(boto3.client("logs", region_name=region))

    @property
    def _function_arn(self) -> str:
        return (
            f"arn:aws:lambda:{self._region}:{self._account_id}"
            f":function:{self._name}"
        )

    def setup(self, name: str) -> None:
        """Create IAM role and CloudWatch log group."""
        self._name = name
        self._role_arn = self._iam.ensure_lambda_role(name)
        self._logs.ensure_log_group(f"/aws/lambda/{name}")

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.replace("_", "-").lower()

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy Lambda and configure trigger."""
        name = self._sanitize_name(name)
        print(settings.INFO_ALERT, f"Deploying '{name}'...")

        self.setup(name)
        image_uri = self._ecr.push(name)
        self._create_or_update_lambda(name, image_uri, self._role_arn)
        self._configure_trigger(name, **kwargs)

        print(settings.INFO_ALERT, "Done.")

    def _create_or_update_lambda(
        self, name: str, image_uri: str, role_arn: str
    ):
        """Create or update Lambda function."""
        try:
            self._lambda.get_function(FunctionName=name)
            print(f"  {settings.STEP_ICON} Updating Lambda function...")
            self._lambda.update_function_code(
                FunctionName=name, ImageUri=image_uri
            )
        except self._lambda.exceptions.ResourceNotFoundException:
            print(f"  {settings.STEP_ICON} Creating Lambda function...")
            self._lambda.create_function(
                FunctionName=name,
                PackageType="Image",
                Code={"ImageUri": image_uri},
                Role=role_arn,
                Timeout=900,
                MemorySize=512,
            )

    def _configure_trigger(self, name: str, **kwargs) -> None:
        """Override in subclasses to configure the specific trigger."""
