"""Lambda + SQS Trigger deployment."""

from __future__ import annotations

from rich import print  # type: ignore

from dotflow.cloud.aws.deployers.base_lambda_deployer import BaseLambdaDeployer
from dotflow.settings import Settings as settings


class LambdaSQSDeployer(BaseLambdaDeployer):
    """Deploy dotflow pipeline as Lambda + SQS Trigger."""

    def _configure_trigger(self, name: str, **kwargs) -> None:
        """Create SQS queue and event source mapping."""
        sqs = self._boto3.client("sqs", region_name=self._region)
        queue_name = f"{name}-queue"

        print(f"  {settings.STEP_ICON} Creating SQS queue '{queue_name}'...")
        try:
            response = sqs.create_queue(
                QueueName=queue_name,
                Attributes={"VisibilityTimeout": "960"},
            )
            queue_url = response["QueueUrl"]
        except sqs.exceptions.QueueNameAlreadyExists:
            queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]

        queue_arn = sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["QueueArn"]
        )["Attributes"]["QueueArn"]

        existing = self._lambda.list_event_source_mappings(
            FunctionName=name, EventSourceArn=queue_arn
        )["EventSourceMappings"]

        if not existing:
            print(f"  {settings.STEP_ICON} Creating event source mapping...")
            self._lambda.create_event_source_mapping(
                FunctionName=name,
                EventSourceArn=queue_arn,
                BatchSize=1,
                Enabled=True,
            )

        print(f"  {settings.STEP_ICON} Queue: {queue_url}")
