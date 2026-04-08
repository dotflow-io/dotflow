"""GCP API enablement."""

from __future__ import annotations

from dotflow.core.exception import ModuleNotFound


class APIs:
    """Enable GCP APIs via Service Usage SDK."""

    REQUIRED = [
        "cloudbuild.googleapis.com",
        "artifactregistry.googleapis.com",
        "run.googleapis.com",
    ]

    def __init__(self, project: str):
        try:
            from google.cloud import service_usage_v1
        except ImportError:
            raise ModuleNotFound(
                module="google-cloud-service-usage",
                library="dotflow[deploy-gcp]",
            ) from None

        self._client = service_usage_v1.ServiceUsageClient()
        self._project = project

    def enable(self):
        """Enable all required APIs."""
        print("  Enabling APIs...")
        for api in self.REQUIRED:
            name = f"projects/{self._project}/services/{api}"
            try:
                self._client.enable_service(name=name).result()
            except Exception as err:
                if "already enabled" in str(err).lower():
                    continue
                print(f"  Warning: Failed to enable {api}: {err}")
