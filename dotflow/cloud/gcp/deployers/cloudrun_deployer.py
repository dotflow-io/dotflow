"""Cloud Run deployment."""

from __future__ import annotations

from rich import print  # type: ignore

from dotflow.cloud.core import Deployer
from dotflow.cloud.gcp.constants import (
    CREDENTIALS_NOT_FOUND,
    GCP_SDK_NOT_FOUND,
)
from dotflow.cloud.gcp.services.apis import APIs
from dotflow.cloud.gcp.services.artifact_registry import ArtifactRegistry
from dotflow.settings import Settings as settings


class CloudRunDeployer(Deployer):
    """Deploy dotflow pipelines to Google Cloud Run."""

    def __init__(self, region: str = "us-central1", project: str = None):
        try:
            from google.api_core import exceptions
            from google.cloud import run_v2
        except ImportError as err:
            raise SystemExit(GCP_SDK_NOT_FOUND) from err

        self._run_v2 = run_v2
        self._exceptions = exceptions
        self._region = region

        if project:
            self._project = project
        else:
            try:
                import google.auth

                _, self._project = google.auth.default()
            except Exception as err:
                raise SystemExit(CREDENTIALS_NOT_FOUND) from err

        if not self._project:
            raise SystemExit(CREDENTIALS_NOT_FOUND)

        self._registry = ArtifactRegistry(
            project=self._project, region=self._region
        )

    def setup(self, name: str) -> None:
        """Enable required GCP APIs and ensure Cloud Build service account."""
        APIs(self._project).enable()
        self._ensure_cloudbuild_sa()

    def _ensure_cloudbuild_sa(self):
        """Ensure Cloud Build service identity exists."""
        try:
            from google.cloud import service_usage_v1

            print(
                f"  {settings.STEP_ICON} "
                "Ensuring Cloud Build service account..."
            )
            client = service_usage_v1.ServiceUsageClient()
            client.generate_service_identity(
                request={
                    "parent": f"projects/{self._project}"
                    f"/services/cloudbuild.googleapis.com"
                }
            )
        except Exception:
            pass

    @staticmethod
    def _sanitize_name(name: str) -> str:
        return name.replace("_", "-").lower()

    def deploy(self, name: str, **kwargs) -> None:
        """Deploy to Cloud Run via Cloud Build + Run SDK."""
        name = self._sanitize_name(name)
        print(settings.INFO_ALERT, f"Deploying Cloud Run '{name}'...")

        self.setup(name)
        image = self._registry.push(name)
        self._deploy_service(name, image)

        print(settings.INFO_ALERT, "Done.")

    def _deploy_service(self, name: str, image: str):
        """Create or update Cloud Run service."""
        print(f"  {settings.STEP_ICON} Deploying service...")

        client = self._run_v2.ServicesClient()
        parent = f"projects/{self._project}/locations/{self._region}"

        service = self._run_v2.Service(
            template=self._run_v2.RevisionTemplate(
                containers=[
                    self._run_v2.Container(image=image),
                ],
            ),
        )

        try:
            request = self._run_v2.CreateServiceRequest(
                parent=parent, service=service, service_id=name
            )
            operation = client.create_service(request=request)
            operation.result()
        except self._exceptions.AlreadyExists:
            print(f"  {settings.STEP_ICON} Updating existing service...")
            service.name = f"{parent}/services/{name}"
            request = self._run_v2.UpdateServiceRequest(service=service)
            operation = client.update_service(request=request)
            operation.result()
