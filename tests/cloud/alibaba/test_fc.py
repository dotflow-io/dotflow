"""Test Alibaba FC deployer."""

import unittest
from unittest.mock import MagicMock, patch

import pytest

try:
    from dotflow.cloud.alibaba.deployers.fc import (
        AliyunFCDeployer,
    )
except ImportError:
    AliyunFCDeployer = None

skip_no_sdk = pytest.mark.skipif(
    AliyunFCDeployer is None,
    reason="alibabacloud SDK not installed",
)


@skip_no_sdk
class TestAliyunFCDeployer(unittest.TestCase):
    def test_sanitize_name(self):
        self.assertEqual(
            AliyunFCDeployer._sanitize_name("my_project"),
            "my-project",
        )

    def test_sanitize_name_lowercase(self):
        self.assertEqual(
            AliyunFCDeployer._sanitize_name("My_Project"),
            "my-project",
        )

    def test_sanitize_name_already_clean(self):
        self.assertEqual(
            AliyunFCDeployer._sanitize_name("my-project"),
            "my-project",
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
    def test_init_with_env(self, mock_config, mock_client):
        deployer = AliyunFCDeployer(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        self.assertEqual(deployer._region, "cn-hangzhou")
        self.assertEqual(deployer._namespace, "dotflow")

    @patch.dict(
        "os.environ",
        {
            "ALIBABA_CLOUD_ACCESS_KEY_ID": "test-key",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "test-secret",
        },
    )
    @patch("alibabacloud_fc_open20210406.client.Client")
    @patch("alibabacloud_tea_openapi.models.Config")
    def test_deploy_calls_push_and_create(self, mock_config, mock_client):
        deployer = AliyunFCDeployer(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        deployer._cr = MagicMock()
        deployer._cr.push.return_value = "img:latest"
        deployer._create_or_update_function = MagicMock()

        deployer.deploy("test_project")

        deployer._cr.push.assert_called_once_with("test-project")
        deployer._create_or_update_function.assert_called_once_with(
            "test-project", "img:latest"
        )
