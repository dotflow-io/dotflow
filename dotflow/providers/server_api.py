"""ServerAPI — sends workflow/task events to a remote HTTP endpoint."""

from __future__ import annotations

import logging
from typing import Any

from requests import patch, post
from requests.exceptions import RequestException

from dotflow.abc.server import Server

logger = logging.getLogger(__name__)


class ServerAPI(Server):
    """HTTP implementation of the Server ABC."""

    def __init__(
        self,
        base_url: str,
        user_token: str,
        timeout: float = 15.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._user_token = user_token
        self._timeout = timeout

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._user_token}",
            "Content-Type": "application/json",
        }

    def _post(self, url: str, json: dict) -> None:
        try:
            response = post(
                url,
                json=json,
                headers=self._headers,
                timeout=self._timeout,
            )
            logger.info("POST %s [%s]", url, response.status_code)
        except RequestException as error:
            logger.error("POST %s failed: %s", url, error)

    def _patch(self, url: str, json: dict) -> None:
        try:
            response = patch(
                url,
                json=json,
                headers=self._headers,
                timeout=self._timeout,
            )
            logger.info("PATCH %s [%s]", url, response.status_code)
        except RequestException as error:
            logger.error("PATCH %s failed: %s", url, error)

    def create_workflow(self, workflow: Any) -> None:
        self._post(
            f"{self._base_url}/workflows",
            json={"id": str(workflow)},
        )

    def update_workflow(self, workflow: Any, status: str = "") -> None:
        self._patch(
            f"{self._base_url}/workflows/{workflow}",
            json={"status": status},
        )

    def create_task(self, task: Any) -> None:
        data = task.result(max=5_000_000)
        data["id"] = data.pop("task_id", task.task_id)
        self._post(
            f"{self._base_url}/workflows/{task.workflow_id}/tasks",
            json=data,
        )

    def update_task(self, task: Any) -> None:
        data = task.result(max=5_000_000)
        self._patch(
            (
                f"{self._base_url}/workflows/{task.workflow_id}"
                f"/tasks/{task.task_id}"
            ),
            json=data,
        )
