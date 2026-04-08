"""Test LambdaSQSDeployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.aws.lambda_sqs_deployer import LambdaSQSDeployer
from dotflow.cloud.core import Deployer


class _QueueExists(Exception):
    pass


class TestLambdaSQSDeployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(LambdaSQSDeployer, "__init__", return_value=None):
            deployer = LambdaSQSDeployer()
        deployer._region = "us-east-1"
        deployer._account_id = "123456789012"
        deployer._name = "test"
        deployer._boto3 = MagicMock()
        deployer._lambda = MagicMock()
        deployer._ecr = MagicMock()
        deployer._iam = MagicMock()
        deployer._logs = MagicMock()
        return deployer

    def test_instance(self):
        deployer = self._make_deployer()
        self.assertIsInstance(deployer, Deployer)

    def test_deploy_creates_queue_and_mapping(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        mock_sqs = MagicMock()
        mock_sqs.create_queue.return_value = {
            "QueueUrl": "https://sqs/test-queue"
        }
        mock_sqs.get_queue_attributes.return_value = {
            "Attributes": {"QueueArn": "arn:aws:sqs:us-east-1:123:test-queue"}
        }
        deployer._boto3.client.return_value = mock_sqs
        deployer._lambda.list_event_source_mappings.return_value = {
            "EventSourceMappings": []
        }

        deployer.deploy("test")

        mock_sqs.create_queue.assert_called_once()
        deployer._lambda.create_event_source_mapping.assert_called_once()

    def test_deploy_skips_existing_mapping(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        mock_sqs = MagicMock()
        mock_sqs.create_queue.return_value = {
            "QueueUrl": "https://sqs/test-queue"
        }
        mock_sqs.get_queue_attributes.return_value = {
            "Attributes": {"QueueArn": "arn:aws:sqs:us-east-1:123:test-queue"}
        }
        deployer._boto3.client.return_value = mock_sqs
        deployer._lambda.list_event_source_mappings.return_value = {
            "EventSourceMappings": [{"UUID": "existing"}]
        }

        deployer.deploy("test")

        deployer._lambda.create_event_source_mapping.assert_not_called()
