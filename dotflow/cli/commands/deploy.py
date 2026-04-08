"""Command deploy module."""

from rich import print  # type: ignore

from dotflow.cli.command import Command
from dotflow.settings import Settings as settings

SAM_PLATFORMS = {
    "ecs-scheduled",
}

DEFAULT_REGIONS = {
    "lambda": "us-east-1",
    "lambda-scheduled": "us-east-1",
    "lambda-s3-trigger": "us-east-1",
    "lambda-sqs-trigger": "us-east-1",
    "lambda-api-trigger": "us-east-1",
    "ecs": "us-east-1",
    "cloud-run": "us-central1",
    "cloud-run-scheduled": "us-central1",
}


class DeployCommand(Command):

    def setup(self):
        platform = self.params.platform
        name = self.params.project
        region = self.params.region or DEFAULT_REGIONS.get(
            platform, "us-east-1"
        )
        schedule = getattr(self.params, "schedule", None)

        if platform in SAM_PLATFORMS:
            print(
                settings.INFO_ALERT,
                f"'{platform}' requires SAM for full trigger setup.",
            )
            print("  Run: sam build && sam deploy")
            return

        deployers = {
            "lambda": self._deploy_lambda,
            "lambda-scheduled": self._deploy_lambda,
            "lambda-s3-trigger": self._deploy_lambda_s3,
            "lambda-sqs-trigger": self._deploy_lambda_sqs,
            "lambda-api-trigger": self._deploy_lambda_api,
            "ecs": self._deploy_ecs,
            "cloud-run": self._deploy_cloud_run,
            "cloud-run-scheduled": self._deploy_cloud_run,
            "github-actions": self._deploy_github_actions,
        }

        handler = deployers.get(platform)
        if not handler:
            print(
                settings.ERROR_ALERT,
                f"Deploy not supported for '{platform}'.",
            )
            return

        handler(name=name, region=region, schedule=schedule)

    def _deploy_lambda(self, name: str, region: str, schedule: str = None):
        """Deploy to AWS Lambda."""
        from dotflow.cloud.aws import LambdaDeployer

        deployer = LambdaDeployer(region=region)
        deployer.deploy(name, schedule=schedule)

    def _deploy_lambda_api(self, name: str, region: str, **kwargs):
        """Deploy to AWS Lambda + API Gateway."""
        from dotflow.cloud.aws import LambdaApiDeployer

        deployer = LambdaApiDeployer(region=region)
        deployer.deploy(name)

    def _deploy_lambda_s3(self, name: str, region: str, **kwargs):
        """Deploy to AWS Lambda + S3 Trigger."""
        from dotflow.cloud.aws import LambdaS3Deployer

        deployer = LambdaS3Deployer(region=region)
        deployer.deploy(name)

    def _deploy_lambda_sqs(self, name: str, region: str, **kwargs):
        """Deploy to AWS Lambda + SQS Trigger."""
        from dotflow.cloud.aws import LambdaSQSDeployer

        deployer = LambdaSQSDeployer(region=region)
        deployer.deploy(name)

    def _deploy_ecs(self, name: str, region: str, **kwargs):
        """Deploy to AWS ECS Fargate."""
        from dotflow.cloud.aws import ECSDeployer

        deployer = ECSDeployer(region=region)
        deployer.deploy(name)

    def _deploy_cloud_run(self, name: str, region: str, **kwargs):
        """Deploy to Google Cloud Run."""
        from dotflow.cloud.gcp import CloudRunDeployer

        deployer = CloudRunDeployer(region=region)
        deployer.deploy(name)

    def _deploy_github_actions(self, name: str, **kwargs):
        """Deploy to GitHub Actions."""
        from dotflow.cloud.github import ActionsDeployer

        deployer = ActionsDeployer()
        deployer.deploy(name)
