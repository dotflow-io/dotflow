"""ECR operations — build, push and authenticate Docker images."""

from __future__ import annotations

import base64
import contextlib
from subprocess import run

from rich import print  # type: ignore

from dotflow.cloud.core import Registry
from dotflow.settings import Settings as settings


class ECR(Registry):
    """Amazon ECR container registry."""

    def __init__(self, ecr_client, account_id: str, region: str):
        self._ecr = ecr_client
        self._account_id = account_id
        self._region = region

    def push(self, name: str) -> str:
        """Build, tag and push a Docker image. Returns the image URI."""
        self._ensure_repository(name)
        self.login()

        image_uri = (
            f"{self._account_id}.dkr.ecr.{self._region}"
            f".amazonaws.com/{name}:latest"
        )

        print(f"  {settings.STEP_ICON} Building image...")
        run(["docker", "build", "-t", name, "."], check=True)

        print(f"  {settings.STEP_ICON} Tagging image...")
        run(["docker", "tag", f"{name}:latest", image_uri], check=True)

        print(f"  {settings.STEP_ICON} Pushing image...")
        run(["docker", "push", image_uri], check=True)

        return image_uri

    def _ensure_repository(self, name: str):
        """Create ECR repository if it doesn't exist."""
        print(f"  {settings.STEP_ICON} Creating ECR repository...")
        with contextlib.suppress(
            self._ecr.exceptions.RepositoryAlreadyExistsException
        ):
            self._ecr.create_repository(repositoryName=name)

    def login(self):
        """Authenticate Docker with ECR."""
        print(f"  {settings.STEP_ICON} Logging in to ECR...")
        token = self._ecr.get_authorization_token()
        auth = token["authorizationData"][0]
        registry = auth["proxyEndpoint"]
        username, password = (
            base64.b64decode(auth["authorizationToken"]).decode().split(":")
        )

        run(
            [
                "docker",
                "login",
                "--username",
                username,
                "--password-stdin",
                registry,
            ],
            input=password,
            text=True,
            capture_output=True,
            check=True,
        )
