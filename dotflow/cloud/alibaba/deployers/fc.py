"""Alibaba Function Compute deployment."""

from __future__ import annotations

import os

from rich import print  # type: ignore

from dotflow.cloud.alibaba.constants import (
    CREDENTIALS_NOT_FOUND,
    SDK_NOT_FOUND,
)
from dotflow.cloud.alibaba.services.cr import ContainerRegistry
from dotflow.cloud.core import Deployer
from dotflow.settings import Settings as settings


class AliyunFCDeployer(Deployer):
    """Deploy dotflow pipeline to Alibaba Cloud FC."""

    def __init__(
        self,
        region: str = "cn-hangzhou",
        namespace: str = "dotflow",
    ):
        try:
            from alibabacloud_fc_open20210406.client import (
                Client,
            )
            from alibabacloud_tea_openapi.models import (
                Config,
            )
        except ImportError as err:
            raise SystemExit(SDK_NOT_FOUND) from err

        key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

        if not key_id or not key_secret:
            try:
                import json
                from pathlib import Path

                config_path = Path.home() / ".aliyun" / "config.json"
                data = json.loads(config_path.read_text())
                for p in data.get("profiles", []):
                    if p.get("name") == data.get("current"):
                        key_id = p.get("access_key_id")
                        key_secret = p.get("access_key_secret")
                        if not region or region == "cn-hangzhou":
                            region = p.get("region_id", region)
                        break
            except Exception:
                pass

        if not key_id or not key_secret:
            raise SystemExit(CREDENTIALS_NOT_FOUND)

        self._region = region
        self._namespace = namespace

        config = Config(
            access_key_id=key_id,
            access_key_secret=key_secret,
            region_id=region,
        )
        config.endpoint = f"{self._region}.fc.aliyuncs.com"
        self._fc = Client(config)

        self._cr = ContainerRegistry(
            region=region,
            namespace=namespace,
        )

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.replace("_", "-").lower()

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy to Alibaba Function Compute."""
        name = self._sanitize_name(name)
        print(
            settings.INFO_ALERT,
            f"Deploying to Alibaba FC '{name}'...",
        )

        image_uri = self._cr.push(name)
        self._create_or_update_function(name, image_uri)

        print(settings.INFO_ALERT, "Done.")

    def _create_or_update_function(self, name: str, image_uri: str) -> None:
        """Create or update FC function."""
        from alibabacloud_fc_open20210406 import models

        try:
            self._fc.get_function(name)
            print(f"  {settings.STEP_ICON} Updating function '{name}'...")
            self._fc.update_function(
                name,
                models.UpdateFunctionRequest(
                    runtime="custom-container",
                    handler="handler.handler",
                    timeout=900,
                    memory_size=512,
                    custom_container_config=(
                        models.CustomContainerConfig(
                            image=image_uri,
                            port=9000,
                        )
                    ),
                ),
            )
        except Exception:
            print(f"  {settings.STEP_ICON} Creating function '{name}'...")
            self._fc.create_function(
                models.CreateFunctionRequest(
                    function_name=name,
                    runtime="custom-container",
                    handler="handler.handler",
                    timeout=900,
                    cpu=1,
                    memory_size=512,
                    disk_size=512,
                    custom_container_config=(
                        models.CustomContainerConfig(
                            image=image_uri,
                            port=9000,
                        )
                    ),
                )
            )
