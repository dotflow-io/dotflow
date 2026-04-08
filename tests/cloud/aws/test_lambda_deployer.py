"""Test LambdaDeployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.aws.lambda_deployer import LambdaDeployer
from dotflow.cloud.core import Deployer


class _ResourceNotFound(Exception):
    pass


class _ResourceConflict(Exception):
    pass


class TestLambdaDeployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(LambdaDeployer, "__init__", return_value=None):
            deployer = LambdaDeployer()
        deployer._region = "us-east-1"
        deployer._account_id = "123456789012"
        deployer._name = "test"
        deployer._boto3 = MagicMock()
        deployer._lambda = MagicMock()
        deployer._lambda.exceptions.ResourceNotFoundException = (
            _ResourceNotFound
        )
        deployer._lambda.exceptions.ResourceConflictException = (
            _ResourceConflict
        )
        deployer._ecr = MagicMock()
        deployer._iam = MagicMock()
        deployer._logs = MagicMock()
        return deployer

    def test_instance(self):
        deployer = self._make_deployer()
        self.assertIsInstance(deployer, Deployer)

    def test_deploy_creates_function(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"
        deployer._lambda.get_function.side_effect = _ResourceNotFound()

        deployer.deploy("test")

        deployer._lambda.create_function.assert_called_once()

    def test_deploy_updates_existing(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        deployer.deploy("test")

        deployer._lambda.update_function_code.assert_called_once()

    def test_deploy_with_schedule(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"
        mock_events = MagicMock()
        deployer._boto3.client.return_value = mock_events

        deployer.deploy("test", schedule="rate(6 hours)")

        mock_events.put_rule.assert_called_once()

    def test_deploy_without_schedule(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        deployer.deploy("test")

        deployer._boto3.client.assert_not_called()
