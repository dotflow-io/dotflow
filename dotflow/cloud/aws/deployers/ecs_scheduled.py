"""ECS Scheduled deployment."""

from __future__ import annotations

from rich import print  # type: ignore

from dotflow.cloud.aws.deployers.ecs import ECSDeployer
from dotflow.settings import Settings as settings


class ECSScheduledDeployer(ECSDeployer):
    """Deploy dotflow pipeline as ECS Fargate + EventBridge schedule."""

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy ECS task and configure EventBridge schedule."""
        name = self._sanitize_name(name)
        schedule = kwargs.get("schedule")

        print(
            settings.INFO_ALERT,
            f"Deploying ECS scheduled task '{name}'...",
        )

        self.setup(name)
        self._ecr.push(name)
        self._create_task_definition(name, self._execution_role_arn)

        if schedule:
            self._configure_schedule(name, schedule)

        print(settings.INFO_ALERT, "Done.")

    def _configure_schedule(self, name: str, schedule: str) -> None:
        """Create EventBridge rule to run ECS task on schedule."""
        import boto3

        events = boto3.client("events", region_name=self._region)
        rule_name = f"{name}-schedule"

        print(
            f"  {settings.STEP_ICON} "
            f"Creating EventBridge rule '{rule_name}'..."
        )

        events.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule,
            State="ENABLED",
        )

        cluster_arn = (
            f"arn:aws:ecs:{self._region}:"
            f"{self._account_id}:"
            f"cluster/{name}-cluster"
        )
        task_def_arn = (
            f"arn:aws:ecs:{self._region}:"
            f"{self._account_id}:"
            f"task-definition/{name}"
        )

        self._ensure_events_role(name)

        events.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    "Id": "1",
                    "Arn": cluster_arn,
                    "RoleArn": (
                        f"arn:aws:iam::{self._account_id}"
                        f":role/{name}-events-role"
                    ),
                    "EcsParameters": {
                        "TaskDefinitionArn": task_def_arn,
                        "TaskCount": 1,
                        "LaunchType": "FARGATE",
                        "NetworkConfiguration": {
                            "awsvpcConfiguration": {
                                "Subnets": self._get_default_subnets(),
                                "AssignPublicIp": "ENABLED",
                            }
                        },
                    },
                }
            ],
        )

        print(f"  {settings.STEP_ICON} Cron: {schedule}")

    def _ensure_events_role(self, name: str) -> str:
        """Create IAM role for EventBridge to run ECS tasks."""
        import json

        role_name = f"{name}-events-role"
        iam = self._iam

        try:
            response = iam._iam.get_role(RoleName=role_name)
            return response["Role"]["Arn"]
        except iam._iam.exceptions.NoSuchEntityException:
            pass

        print(
            f"  {settings.STEP_ICON} "
            f"Creating EventBridge role '{role_name}'..."
        )

        response = iam._iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "events.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )

        iam._iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=("arn:aws:iam::aws:policy/AmazonECS_FullAccess"),
        )
        iam._iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=("arn:aws:iam::aws:policy/CloudWatchEventsFullAccess"),
        )

        import time

        time.sleep(10)
        return response["Role"]["Arn"]

    def _get_default_subnets(self) -> list[str]:
        """Get default VPC subnets."""
        import boto3

        ec2 = boto3.client("ec2", region_name=self._region)
        vpcs = ec2.describe_vpcs(
            Filters=[{"Name": "isDefault", "Values": ["true"]}]
        )
        if not vpcs["Vpcs"]:
            return []

        vpc_id = vpcs["Vpcs"][0]["VpcId"]
        subnets = ec2.describe_subnets(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )
        return [s["SubnetId"] for s in subnets["Subnets"]]
