"""Alibaba Container Registry operations."""

from __future__ import annotations

import json
import os
from pathlib import Path
from subprocess import run

from rich import print  # type: ignore

from dotflow.cloud.core import Registry
from dotflow.settings import Settings as settings


class ContainerRegistry(Registry):
    """Build and push Docker images to Alibaba CR."""

    def __init__(self, region: str, namespace: str):
        self._region = region
        self._namespace = namespace
        self._registry = f"registry.{region}.aliyuncs.com"
        self._credentials = self._load_credentials()

    def push(self, name: str) -> str:
        """Build, tag, and push image."""
        image_uri = f"{self._registry}/{self._namespace}/{name}:latest"

        print(f"  {settings.STEP_ICON} Building image...")
        run(
            ["docker", "build", "-t", name, "."],
            check=True,
        )

        print(f"  {settings.STEP_ICON} Tagging image...")
        run(
            ["docker", "tag", name, image_uri],
            check=True,
        )

        self.login()

        print(f"  {settings.STEP_ICON} Pushing image...")
        run(
            ["docker", "push", image_uri],
            check=True,
        )

        return image_uri

    def login(self) -> None:
        """Login to Alibaba CR."""
        print(f"  {settings.STEP_ICON} Logging in to {self._registry}...")
        key_id, _ = self._credentials
        password = os.environ.get("ALIBABA_CR_PASSWORD", "")

        if not password:
            raise SystemExit(
                "Set ALIBABA_CR_PASSWORD env var. "
                "Configure at: Container Registry "
                "> Access Credential > Set Password"
            )

        run(
            [
                "docker",
                "login",
                "--username",
                key_id,
                "--password-stdin",
                self._registry,
            ],
            input=password,
            check=True,
        )

    @staticmethod
    def _load_credentials() -> tuple[str, str]:
        """Load credentials from env or aliyun config."""
        key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
        key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

        if key_id and key_secret:
            return key_id, key_secret

        try:
            config_path = Path.home() / ".aliyun" / "config.json"
            data = json.loads(config_path.read_text())
            for p in data.get("profiles", []):
                if p.get("name") == data.get("current"):
                    return (
                        p.get("access_key_id", ""),
                        p.get("access_key_secret", ""),
                    )
        except Exception:
            pass

        return "", ""
