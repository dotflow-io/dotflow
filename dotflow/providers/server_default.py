"""ServerDefault

Default implementation that communicates with a
dotflow-api server.

Args:
    base_url (str): Base URL of the API.
    user_token (str): API token (X-User-Token header).
    timeout (float): HTTP request timeout in seconds.
"""

from __future__ import annotations

from typing import Any

from requests import patch as http_patch
from requests import post as http_post

from dotflow.abc.server import Server
from dotflow.logging import logger


class ServerDefault(Server):
    """Default Server implementation (HTTP client)."""

    def __init__(
        self,
        base_url: str = "",
        user_token: str = "",
        timeout: float = 5.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.user_token = user_token
        self.timeout = timeout
        self.enabled = bool(self.base_url and self.user_token)

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-User-Token": self.user_token,
        }

    def _request(self, method, url, payload=None):
        try:
            response = method(
                url=url,
                headers=self._headers(),
                json=payload or {},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except Exception as error:
            logger.error(
                "Server %s failed: %s",
                url,
                str(error),
            )

    def create_workflow(self, workflow: Any) -> None:
        """Create workflow record (synchronous)."""
        if not self.enabled:
            return

        self._request(
            http_post,
            f"{self.base_url}/workflows",
            {
                "id": f"{workflow}",
                "execution_mode": "sequential",
                "keep_going": False,
            },
        )

    def update_workflow(self, workflow: Any, status: str = "") -> None:
        """Update workflow status (synchronous)."""
        if not self.enabled:
            return

        self._request(
            http_patch,
            f"{self.base_url}/workflows/{workflow}",
            {"status": status},
        )

    def create_task(self, task: Any) -> None:
        """Create a task under a workflow (synchronous)."""
        if not self.enabled:
            return

        payload = {
            "id": task.task_id,
            "initial_context": (task.initial_context.storage),
            "group_name": (task.group_name or "default"),
        }

        self._request(
            http_post,
            f"{self.base_url}/workflows/{task.workflow_id}/tasks",
            payload,
        )

    def update_task(self, task: Any) -> None:
        """Update task data (synchronous)."""
        if not self.enabled:
            return

        self._request(
            http_patch,
            f"{self.base_url}/workflows/"
            f"{task.workflow_id}/tasks/{task.task_id}",
            task.result(),
        )
