"""IAM operations — create and manage execution roles."""

from __future__ import annotations

import json
import time

from dotflow.cloud.core import RoleManager


class IAM(RoleManager):
    """AWS IAM role manager."""

    def __init__(self, iam_client):
        self._iam = iam_client

    def ensure_lambda_role(self, name: str) -> str:
        """Create or get Lambda execution role."""
        return self.ensure_role(
            name=f"{name}-lambda-role",
            service="lambda.amazonaws.com",
            policy=(
                "arn:aws:iam::aws:policy/service-role/"
                "AWSLambdaBasicExecutionRole"
            ),
            wait=True,
        )

    def ensure_ecs_execution_role(self) -> str:
        """Create or get ECS task execution role."""
        return self.ensure_role(
            name="ecsTaskExecutionRole",
            service="ecs-tasks.amazonaws.com",
            policy=(
                "arn:aws:iam::aws:policy/service-role/"
                "AmazonECSTaskExecutionRolePolicy"
            ),
        )

    def ensure_role(
        self,
        name: str,
        service: str,
        policy: str,
        wait: bool = False,
    ) -> str:
        """Create role if it doesn't exist, attach policy, return ARN."""
        role_name = name
        try:
            response = self._iam.get_role(RoleName=role_name)
            return response["Role"]["Arn"]
        except self._iam.exceptions.NoSuchEntityException:
            pass

        print(f"  Creating IAM role '{role_name}'...")
        response = self._iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": service},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
        self._iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy,
        )

        if wait:
            time.sleep(10)

        return response["Role"]["Arn"]
