"""ECS deployment."""

from __future__ import annotations

import json
from pathlib import Path

from rich import print  # type: ignore

from dotflow.cloud.aws.constants import BOTO3_NOT_FOUND, CREDENTIALS_NOT_FOUND
from dotflow.cloud.aws.services.cloudwatch import CloudWatch
from dotflow.cloud.aws.services.ecr import ECR
from dotflow.cloud.aws.services.iam import IAM
from dotflow.cloud.core import Deployer
from dotflow.settings import Settings as settings


class ECSDeployer(Deployer):
    """Deploy dotflow pipelines to AWS ECS Fargate."""

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
        self._ecs = boto3.client("ecs", region_name=region)

        self._ecr = ECR(
            boto3.client("ecr", region_name=region),
            self._account_id,
            region,
        )
        self._iam = IAM(boto3.client("iam", region_name=region))
        self._logs = CloudWatch(boto3.client("logs", region_name=region))

    def setup(self, name: str) -> None:
        """Create IAM role, CloudWatch log group, and ECS cluster."""
        self._execution_role_arn = self._iam.ensure_ecs_execution_role()
        self._logs.ensure_log_group(f"/ecs/{name}")
        self._ensure_cluster(name)

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy an ECS Fargate task from the current directory."""
        print(settings.INFO_ALERT, f"Deploying ECS task '{name}'...")

        self.setup(name)
        self._ecr.push(name)

        if (Path.cwd() / "task-definition.json").exists():
            self._register_from_file()
        else:
            self._create_task_definition(name, self._execution_role_arn)

        print(settings.INFO_ALERT, "Done.")

    def _register_from_file(self):
        """Register task definition from task-definition.json."""
        content = json.loads((Path.cwd() / "task-definition.json").read_text())
        print(f"  {settings.STEP_ICON} Registering task definition...")
        self._ecs.register_task_definition(**content)

    def _create_task_definition(self, name: str, execution_role_arn: str):
        """Create a basic Fargate task definition."""
        image_uri = (
            f"{self._account_id}.dkr.ecr.{self._region}"
            f".amazonaws.com/{name}:latest"
        )
        print(f"  {settings.STEP_ICON} Creating task definition...")
        self._ecs.register_task_definition(
            family=name,
            networkMode="awsvpc",
            requiresCompatibilities=["FARGATE"],
            cpu="256",
            memory="512",
            executionRoleArn=execution_role_arn,
            containerDefinitions=[
                {
                    "name": name,
                    "image": image_uri,
                    "essential": True,
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": f"/ecs/{name}",
                            "awslogs-region": self._region,
                            "awslogs-stream-prefix": "ecs",
                        },
                    },
                }
            ],
        )

    def _ensure_cluster(self, name: str):
        """Create ECS cluster if it doesn't exist."""
        cluster_name = f"{name}-cluster"
        clusters = self._ecs.describe_clusters(clusters=[cluster_name])
        active = [c for c in clusters["clusters"] if c["status"] == "ACTIVE"]
        if not active:
            print(
                f"  {settings.STEP_ICON} "
                f"Creating ECS cluster '{cluster_name}'..."
            )
            self._ecs.create_cluster(clusterName=cluster_name)
