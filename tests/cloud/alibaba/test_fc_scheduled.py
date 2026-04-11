"""Test Alibaba FC Scheduled deployer."""

import unittest
from unittest.mock import MagicMock

import pytest

try:
    import alibabacloud_fc_open20210406  # noqa: F401

    HAS_SDK = True
except ImportError:
    HAS_SDK = False

skip_no_sdk = pytest.mark.skipif(
    not HAS_SDK,
    reason="alibabacloud SDK not installed",
)


@skip_no_sdk
class TestAliyunFCScheduledDeployer(unittest.TestCase):
    @unittest.mock.patch.dict(
        "os.environ",
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "test-key",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "test-secret",
        },
    )
    @unittest.mock.patch("alibabacloud_fc_open20210406.client.Client")
    @unittest.mock.patch("alibabacloud_tea_openapi.models.Config")
    def test_deploy_with_schedule(self, mock_config, mock_client):
        from dotflow.cloud.alibaba.deployers.fc_scheduled import (
            AliyunFCScheduledDeployer,
        )

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

    @unittest.mock.patch.dict(
        "os.environ",
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "test-key",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "test-secret",
        },
    )
    @unittest.mock.patch("alibabacloud_fc_open20210406.client.Client")
    @unittest.mock.patch("alibabacloud_tea_openapi.models.Config")
    def test_deploy_without_schedule(self, mock_config, mock_client):
        from dotflow.cloud.alibaba.deployers.fc_scheduled import (
            AliyunFCScheduledDeployer,
        )

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
