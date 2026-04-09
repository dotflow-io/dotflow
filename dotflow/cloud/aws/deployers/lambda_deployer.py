"""Lambda deployment."""

from __future__ import annotations

import contextlib

from dotflow.cloud.aws.deployers.base_lambda_deployer import BaseLambdaDeployer


class LambdaDeployer(BaseLambdaDeployer):
    """Deploy dotflow pipelines to AWS Lambda."""

    def _configure_trigger(self, name: str, **kwargs) -> None:
        """Create EventBridge schedule if provided."""
        schedule = kwargs.get("schedule")
        if not schedule:
            return

        rule_name = f"{name}-schedule"

        print(f"  Creating EventBridge rule '{rule_name}'...")
        events = self._boto3.client("events", region_name=self._region)

        events.put_rule(
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

        events.put_targets(
            Rule=rule_name,
            Targets=[{"Id": "1", "Arn": self._function_arn}],
        )

        print(f"  Schedule: {schedule}")
