"""Test Alibaba FC Scheduled deployer."""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.cloud.alibaba.deployers.fc_scheduled import (
    AliyunFCScheduledDeployer,
)


class TestAliyunFCScheduledDeployer(unittest.TestCase):
    @patch.dict(
        "os.environ",
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "test-key",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "test-secret",
        },
    )
    @patch("alibabacloud_fc_open20210406.client.Client")
    @patch("alibabacloud_tea_openapi.models.Config")
    def test_deploy_with_schedule(self, mock_config, mock_client):
        deployer = AliyunFCScheduledDeployer(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        deployer._cr = MagicMock()
        deployer._cr.push.return_value = "img:latest"
        deployer._create_or_update_function = MagicMock()
        deployer._configure_trigger = MagicMock()

        deployer.deploy("test-project", schedule="0 */6 * * *")

        deployer._cr.push.assert_called_once()
        deployer._create_or_update_function.assert_called_once()
        deployer._configure_trigger.assert_called_once_with(
            "test-project", "0 */6 * * *"
        )

    @patch.dict(
        "os.environ",
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "test-key",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "test-secret",
        },
    )
    @patch("alibabacloud_fc_open20210406.client.Client")
    @patch("alibabacloud_tea_openapi.models.Config")
    def test_deploy_without_schedule(self, mock_config, mock_client):
        deployer = AliyunFCScheduledDeployer(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        deployer._cr = MagicMock()
        deployer._cr.push.return_value = "img:latest"
        deployer._create_or_update_function = MagicMock()
        deployer._configure_trigger = MagicMock()

        deployer.deploy("test-project")

        deployer._configure_trigger.assert_not_called()
