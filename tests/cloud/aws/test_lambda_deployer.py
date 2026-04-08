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
        deployer._lambda = MagicMock()
        deployer._lambda.exceptions.ResourceNotFoundException = (
            _ResourceNotFound
        )
        deployer._lambda.exceptions.ResourceConflictException = (
            _ResourceConflict
        )
        deployer._events = MagicMock()
        deployer._ecr = MagicMock()
        deployer._iam = MagicMock()
        deployer._logs = MagicMock()
        return deployer

    def test_instance(self):
        deployer = self._make_deployer()
        self.assertIsInstance(deployer, Deployer)

    def test_deploy_creates_function(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = (
            "123.dkr.ecr.us-east-1.amazonaws.com/test:latest"
        )
        deployer._iam.ensure_lambda_role.return_value = (
            "arn:aws:iam::123:role/test-lambda-role"
        )
        deployer._lambda.get_function.side_effect = _ResourceNotFound()

        deployer.deploy("test")

        deployer._ecr.push.assert_called_once_with("test")
        deployer._iam.ensure_lambda_role.assert_called_once_with("test")
        deployer._logs.ensure_log_group.assert_called_once()
        deployer._lambda.create_function.assert_called_once()

    def test_deploy_updates_existing_function(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = (
            "123.dkr.ecr.us-east-1.amazonaws.com/test:latest"
        )
        deployer._iam.ensure_lambda_role.return_value = (
            "arn:aws:iam::123:role/test-lambda-role"
        )

        deployer.deploy("test")

        deployer._lambda.update_function_code.assert_called_once()

    def test_deploy_with_schedule(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = (
            "123.dkr.ecr.us-east-1.amazonaws.com/test:latest"
        )
        deployer._iam.ensure_lambda_role.return_value = (
            "arn:aws:iam::123:role/test-lambda-role"
        )

        deployer.deploy("test", schedule="rate(6 hours)")

        deployer._events.put_rule.assert_called_once()
        deployer._events.put_targets.assert_called_once()

    def test_deploy_without_schedule(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        deployer.deploy("test")

        deployer._events.put_rule.assert_not_called()
