"""Command deploy module."""

from rich import print  # type: ignore
from rich.prompt import Prompt

from dotflow.cli.command import Command
from dotflow.cloud.alibaba.constants import (
    DEFAULT_REGION as ALI_DEFAULT_REGION,
)
from dotflow.cloud.alibaba.constants import PLATFORMS as ALI_PLATFORMS
from dotflow.cloud.alibaba.constants import (
    SCHEDULED_PLATFORMS as ALI_SCHEDULED,
)
from dotflow.cloud.aws.constants import DEFAULT_REGION as AWS_DEFAULT_REGION
from dotflow.cloud.aws.constants import PLATFORMS as AWS_PLATFORMS
from dotflow.cloud.aws.constants import SCHEDULED_PLATFORMS as AWS_SCHEDULED
from dotflow.cloud.gcp.constants import DEFAULT_REGION as GCP_DEFAULT_REGION
from dotflow.cloud.gcp.constants import PLATFORMS as GCP_PLATFORMS
from dotflow.cloud.gcp.constants import SCHEDULED_PLATFORMS as GCP_SCHEDULED
from dotflow.settings import Settings as settings

DEFAULT_REGIONS = {
    **dict.fromkeys(AWS_PLATFORMS, AWS_DEFAULT_REGION),
    **dict.fromkeys(GCP_PLATFORMS, GCP_DEFAULT_REGION),
    **dict.fromkeys(ALI_PLATFORMS, ALI_DEFAULT_REGION),
}

SCHEDULED_PLATFORMS = AWS_SCHEDULED | GCP_SCHEDULED | ALI_SCHEDULED


class ScheduleResolver:
    """Resolves a schedule expression.

    From CLI args, template, or user input.
    """

    @classmethod
    def _get_provider(cls, platform: str) -> type | None:
        if platform in AWS_PLATFORMS:
            from dotflow.cloud.aws.schedule import AWSSchedule

            return AWSSchedule

        return None

    @classmethod
    def resolve(cls, schedule: str | None, platform: str) -> str | None:
        if platform not in SCHEDULED_PLATFORMS:
            return schedule

        provider = cls._get_provider(platform)

        if schedule:
            return provider.convert(schedule) if provider else schedule

        raw = cls._ask_schedule(provider)

        if not raw:
            raise SystemExit(
                f"{settings.ERROR_ALERT} --schedule (cron) is required for {platform}"
            )

        return provider.convert(raw) if provider else raw

    @classmethod
    def _ask_schedule(cls, provider: type | None) -> str | None:
        template_schedule = None
        if provider:
            template_schedule = provider.read_from_template()

        choices = {}
        if template_schedule:
            choices["1"] = f"Use from template.yaml: {template_schedule}"
        choices["2"] = "Enter cron expression"

        print(settings.QUESTION_ALERT, "Cron schedule is required:")
        for key, label in choices.items():
            print(f"  [bold cyan]{key}[/bold cyan] - {label}")

        choice = Prompt.ask("  Select", choices=list(choices.keys()))

        if choice == "1" and template_schedule:
            print(settings.INFO_ALERT, f"Using cron: {template_schedule}")
            return template_schedule

        print("  Format: [bold]min hour day month weekday[/bold]")
        return Prompt.ask("  Cron (e.g. */5 * * * *)") or None


class DeployCommand(Command):
    def setup(self):
        platform = self.params.platform
        name = self.params.project
        region = self.params.region or DEFAULT_REGIONS.get(platform)
        schedule = ScheduleResolver.resolve(
            getattr(self.params, "schedule", None), platform
        )

        method_name = f"_deploy_{platform.replace('-', '_')}"
        handler = getattr(self, method_name, None)
        if not handler:
            print(
                settings.ERROR_ALERT, f"Deploy not supported for '{platform}'."
            )
            return

        handler(name=name, region=region, schedule=schedule)

    def _deploy_lambda(self, name, region, schedule=None):
        from dotflow.cloud.aws import LambdaDeployer

        LambdaDeployer(region=region).deploy(name, schedule=schedule)

    def _deploy_lambda_scheduled(self, name, region, schedule=None):
        from dotflow.cloud.aws import LambdaDeployer

        LambdaDeployer(region=region).deploy(name, schedule=schedule)

    def _deploy_lambda_s3_trigger(self, name, region, **kwargs):
        from dotflow.cloud.aws import LambdaS3Deployer

        LambdaS3Deployer(region=region).deploy(name)

    def _deploy_lambda_sqs_trigger(self, name, region, **kwargs):
        from dotflow.cloud.aws import LambdaSQSDeployer

        LambdaSQSDeployer(region=region).deploy(name)

    def _deploy_lambda_api_trigger(self, name, region, **kwargs):
        from dotflow.cloud.aws import LambdaApiDeployer

        LambdaApiDeployer(region=region).deploy(name)

    def _deploy_ecs(self, name, region, **kwargs):
        from dotflow.cloud.aws import ECSDeployer

        ECSDeployer(region=region).deploy(name)

    def _deploy_ecs_scheduled(self, name, region, schedule=None):
        from dotflow.cloud.aws import ECSScheduledDeployer

        ECSScheduledDeployer(region=region).deploy(name, schedule=schedule)

    def _deploy_cloud_run(self, name, region, **kwargs):
        from dotflow.cloud.gcp import CloudRunDeployer

        CloudRunDeployer(region=region).deploy(name)

    def _deploy_cloud_run_scheduled(self, name, region, **kwargs):
        from dotflow.cloud.gcp import CloudRunDeployer

        CloudRunDeployer(region=region).deploy(name)

    def _deploy_github_actions(self, name, **kwargs):
        from dotflow.cloud.github import ActionsDeployer

        ActionsDeployer().deploy(name)

    def _deploy_alibaba_fc(self, name, region, **kwargs):
        from dotflow.cloud.alibaba import AliyunFCDeployer

        AliyunFCDeployer(region=region).deploy(name)

    def _deploy_alibaba_fc_scheduled(self, name, region, schedule=None):
        from dotflow.cloud.alibaba import (
            AliyunFCScheduledDeployer,
        )

        AliyunFCScheduledDeployer(region=region).deploy(
            name, schedule=schedule
        )
