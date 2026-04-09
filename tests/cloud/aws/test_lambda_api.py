"""Test LambdaApiDeployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.aws.deployers.lambda_api import LambdaApiDeployer
from dotflow.cloud.core import Deployer


class _ResourceConflict(Exception):
    pass


class TestLambdaApiDeployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(LambdaApiDeployer, "__init__", return_value=None):
            deployer = LambdaApiDeployer()
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

    def test_deploy_creates_api(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        mock_apigw = MagicMock()
        mock_apigw.get_apis.return_value = {"Items": []}
        mock_apigw.create_api.return_value = {"ApiId": "abc123"}
        mock_apigw.create_integration.return_value = {"IntegrationId": "int1"}
        deployer._boto3.client.return_value = mock_apigw

        deployer.deploy("test")

        mock_apigw.create_api.assert_called_once()
        mock_apigw.create_route.assert_called_once()

    def test_deploy_skips_existing_api(self):
        deployer = self._make_deployer()
        deployer._ecr.push.return_value = "uri"
        deployer._iam.ensure_lambda_role.return_value = "arn"

        mock_apigw = MagicMock()
        mock_apigw.get_apis.return_value = {
            "Items": [{"Name": "test-api", "ApiId": "existing"}]
        }
        deployer._boto3.client.return_value = mock_apigw

        deployer.deploy("test")

        mock_apigw.create_api.assert_not_called()
