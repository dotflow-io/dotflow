"""Test ECSDeployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.aws.deployers.ecs_deployer import ECSDeployer
from dotflow.cloud.core import Deployer


class TestECSDeployer(unittest.TestCase):
    def _make_deployer(self):
        with patch.object(ECSDeployer, "__init__", return_value=None):
            deployer = ECSDeployer()
        deployer._region = "us-east-1"
        deployer._account_id = "123456789012"
        deployer._ecs = MagicMock()
        deployer._ecr = MagicMock()
        deployer._iam = MagicMock()
        deployer._logs = MagicMock()
        return deployer

    def test_instance(self):
        deployer = self._make_deployer()
        self.assertIsInstance(deployer, Deployer)

    def test_setup_creates_role_logs_cluster(self):
        deployer = self._make_deployer()
        deployer._ecs.describe_clusters.return_value = {"clusters": []}

        deployer.setup("test")

        deployer._iam.ensure_ecs_execution_role.assert_called_once()
        deployer._logs.ensure_log_group.assert_called_once_with("/ecs/test")
        deployer._ecs.create_cluster.assert_called_once()

    def test_deploy_with_task_definition_file(self):
        deployer = self._make_deployer()
        deployer._ecs.describe_clusters.return_value = {"clusters": []}

        with patch(
            "dotflow.cloud.aws.deployers.ecs_deployer.Path"
        ) as mock_path:
            mock_path.cwd.return_value.__truediv__ = MagicMock(
                return_value=MagicMock(
                    exists=MagicMock(return_value=True),
                    read_text=MagicMock(return_value='{"family": "test"}'),
                )
            )
            deployer.deploy("test")

        deployer._ecr.push.assert_called_once_with("test")
        deployer._ecs.register_task_definition.assert_called_once()

    def test_deploy_creates_task_definition(self):
        deployer = self._make_deployer()
        deployer._ecs.describe_clusters.return_value = {"clusters": []}
        deployer._iam.ensure_ecs_execution_role.return_value = "arn:role"

        with patch(
            "dotflow.cloud.aws.deployers.ecs_deployer.Path"
        ) as mock_path:
            mock_path.cwd.return_value.__truediv__ = MagicMock(
                return_value=MagicMock(exists=MagicMock(return_value=False))
            )
            deployer.deploy("test")

        deployer._ecs.register_task_definition.assert_called_once()

    def test_ensure_cluster_skips_if_active(self):
        deployer = self._make_deployer()
        deployer._ecs.describe_clusters.return_value = {
            "clusters": [{"status": "ACTIVE"}]
        }

        deployer._ensure_cluster("test")

        deployer._ecs.create_cluster.assert_not_called()
