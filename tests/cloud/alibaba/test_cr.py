"""Test Alibaba Container Registry."""

import unittest

from dotflow.cloud.alibaba.services.cr import (
    ContainerRegistry,
)


class TestContainerRegistry(unittest.TestCase):
    def test_registry_url(self):
        cr = ContainerRegistry(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        self.assertEqual(
            cr._registry,
            "registry.cn-hangzhou.aliyuncs.com",
        )

    def test_image_uri_format(self):
        cr = ContainerRegistry(
            region="cn-hangzhou",
            namespace="dotflow",
        )
        expected = (
            "registry.cn-hangzhou.aliyuncs.com/dotflow/my-project:latest"
        )
        uri = f"{cr._registry}/{cr._namespace}/my-project:latest"
        self.assertEqual(uri, expected)

    def test_load_credentials_from_env(self):
        import os
        from unittest.mock import patch

        with patch.dict(
            os.environ,
            {
                "ALIBABA_CLOUD_ACCESS_KEY_ID": "key",
                "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "secret",
            },
        ):
            key_id, key_secret = ContainerRegistry._load_credentials()
            self.assertEqual(key_id, "key")
            self.assertEqual(key_secret, "secret")

    def test_load_credentials_empty_env(self):
        import os
        from unittest.mock import patch

        with (
            patch.dict(
                os.environ,
                {
                    "ALIBABA_CLOUD_ACCESS_KEY_ID": "",
                    "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "",
                },
                clear=True,
            ),
            patch(
                "pathlib.Path.read_text",
                side_effect=FileNotFoundError,
            ),
        ):
            key_id, key_secret = ContainerRegistry._load_credentials()
            self.assertEqual(key_id, "")
            self.assertEqual(key_secret, "")
