"""Test LambdaS3Deployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.aws.deployers.lambda_s3 import LambdaS3Deployer
from dotflow.cloud.core import Deployer


class _ResourceConflict(Exception):
    pass


class _BucketExists(Exception):
    pass


class TestLambdaS3Deployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(LambdaS3Deployer, "__init__", return_value=None):
            deployer = LambdaS3Deployer()
        deployer._region = "us-east-1"
        deployer._account_id = "123456789012"
        deployer._name = "test"
        deployer._boto3 = MagicMock()
        deployer._lambda = MagicMock()
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

    def test_deploy_creates_bucket_and_notification(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        mock_s3 = MagicMock()
        mock_s3.exceptions.BucketAlreadyOwnedByYou = _BucketExists
        deployer._boto3.client.return_value = mock_s3

        deployer.deploy("test")

        mock_s3.create_bucket.assert_called_once()
        mock_s3.put_bucket_notification_configuration.assert_called_once()
