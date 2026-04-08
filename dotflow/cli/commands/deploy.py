"""Command deploy module."""

from rich import print  # type: ignore

from dotflow.cli.command import Command
from dotflow.settings import Settings as settings

SAM_PLATFORMS = {
    "lambda-s3-trigger",
    "lambda-sqs-trigger",
    "lambda-api-trigger",
    "ecs-scheduled",
}


class DeployCommand(Command):
    def setup(self):
        platform = self.params.platform
        name = self.params.project
        region = self.params.region
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
            "ecs": self._deploy_ecs,
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

    def _deploy_ecs(self, name: str, region: str, **kwargs):
        """Deploy to AWS ECS Fargate."""
        from dotflow.cloud.aws import ECSDeployer

        deployer = ECSDeployer(region=region)
        deployer.deploy(name)
