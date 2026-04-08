"""Artifact Registry operations — build and push Docker images."""

from __future__ import annotations

import io
import os
import tarfile

from dotflow.cloud.core import Registry
from dotflow.core.exception import ModuleNotFound


class ArtifactRegistry(Registry):
    """Google Artifact Registry container registry."""

    def __init__(self, project: str, region: str):
        try:
            from google.cloud import artifactregistry_v1
            from google.cloud import storage as gcs
            from google.cloud.devtools import cloudbuild_v1
        except ImportError:
            raise ModuleNotFound(
                module="google-cloud-build",
                library="dotflow[deploy-gcp]",
            ) from None

        self._cloudbuild = cloudbuild_v1
        self._ar = artifactregistry_v1
        self._gcs = gcs
        self._project = project
        self._region = region
        self._bucket_name = f"{project}_cloudbuild"
        self._image_base = (
            f"{region}-docker.pkg.dev/{project}/cloud-run-source-deploy"
        )

    def login(self) -> None:
        """No-op — Cloud Build handles authentication."""

    def push(self, name: str) -> str:
        """Build and push Docker image via Cloud Build. Returns image URI."""
        image = f"{self._image_base}/{name}:latest"
        object_name = f"source/{name}.tar.gz"

        self._ensure_repository(name)
        self._upload_source(object_name)
        self._build(image, object_name)

        return image

    def _ensure_repository(self, name: str):
        """Create Artifact Registry Docker repository if it doesn't exist."""
        print("  Ensuring Artifact Registry repository...")

        client = self._ar.ArtifactRegistryClient()
        parent = f"projects/{self._project}/locations/{self._region}"
        repo_name = "cloud-run-source-deploy"

        try:
            client.get_repository(name=f"{parent}/repositories/{repo_name}")
        except Exception:
            client.create_repository(
                parent=parent,
                repository=self._ar.Repository(
                    format_=self._ar.Repository.Format.DOCKER,
                    description=f"Docker images for {name}",
                ),
                repository_id=repo_name,
            ).result()

    def _upload_source(self, object_name: str):
        """Tar the current directory and upload to GCS."""
        print("  Uploading source...")

        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            for entry in os.listdir("."):
                if entry.startswith("."):
                    continue
                tar.add(entry)
        buf.seek(0)

        client = self._gcs.Client(project=self._project)
        bucket = client.bucket(self._bucket_name)

        try:
            bucket.reload()
        except Exception:
            bucket.create(location=self._region)

        blob = bucket.blob(object_name)
        blob.upload_from_file(buf, content_type="application/gzip")

    def _build(self, image: str, object_name: str):
        """Build Docker image via Cloud Build."""
        print("  Building and pushing image via Cloud Build...")

        client = self._cloudbuild.CloudBuildClient()

        build = self._cloudbuild.Build(
            source=self._cloudbuild.Source(
                storage_source=self._cloudbuild.StorageSource(
                    bucket=self._bucket_name,
                    object_=object_name,
                )
            ),
            steps=[
                self._cloudbuild.BuildStep(
                    name="gcr.io/cloud-builders/docker",
                    args=["build", "-t", image, "."],
                ),
            ],
            images=[image],
        )

        try:
            operation = client.create_build(
                project_id=self._project,
                build=build,
            )
            print(f"  Build started: {operation.metadata.build.id}")
            result = operation.result(timeout=600)
            print(f"  Build status: {result.status.name}")
        except Exception as err:
            raise SystemExit(
                f"Cloud Build failed: {type(err).__name__}: {err}"
            ) from err
