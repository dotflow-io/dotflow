"""ServerDefault - managed HTTP server provider."""

from __future__ import annotations

from functools import wraps
from typing import Any

from requests import patch, post
from requests.exceptions import RequestException

from dotflow.abc.server import Server
from dotflow.core.config_file import resolve
from dotflow.logging import logger


def managed(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._managed:
            return
        return method(self, *args, **kwargs)

    return wrapper


class ServerDefault(Server):
    """Default Server provider with auto-detected managed mode."""

    MAX_RESULT_SIZE = 5_000_000
    TIMEOUT = 15.0

    ENDPOINT_WORKFLOWS = "/cli/workflows"
    ENDPOINT_WORKFLOW = "/cli/workflows/{workflow_id}"
    ENDPOINT_TASKS = "/cli/workflows/{workflow_id}/tasks"
    ENDPOINT_TASK = "/cli/workflows/{workflow_id}/tasks/{task_id}"

    def __init__(self) -> None:
        base_url = resolve(key="base_url", env_var="SERVER_BASE_URL")
        user_token = resolve(key="token", env_var="SERVER_USER_TOKEN")
        self._managed = bool(base_url and user_token)

        self._base_url = base_url.rstrip("/") if base_url else None
        self._user_token = user_token

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._user_token}",
            "Content-Type": "application/json",
        }

    def _post(self, url: str, json: dict) -> None:
        try:
            post(
                url,
                json=json,
                headers=self._headers,
                timeout=self.TIMEOUT,
            )
        except RequestException as error:
            logger.error("POST %s failed: %s", url, error)

    def _patch(self, url: str, json: dict) -> None:
        try:
            patch(
                url,
                json=json,
                headers=self._headers,
                timeout=self.TIMEOUT,
            )
        except RequestException as error:
            logger.error("PATCH %s failed: %s", url, error)

    @managed
    def create_workflow(self, workflow: Any) -> None:
        self._post(
            self._base_url + self.ENDPOINT_WORKFLOWS,
            json=workflow.result(),
        )

    @managed
    def update_workflow(self, workflow: Any, status: str = "") -> None:
        self._patch(
            self._base_url
            + self.ENDPOINT_WORKFLOW.format(workflow_id=workflow),
            json={"status": status},
        )

    @managed
    def create_task(self, task: Any) -> None:
        self._post(
            self._base_url
            + self.ENDPOINT_TASKS.format(workflow_id=task.workflow_id),
            json=task.result(max=self.MAX_RESULT_SIZE),
        )

    @managed
    def update_task(self, task: Any) -> None:
        self._patch(
            self._base_url
            + self.ENDPOINT_TASK.format(
                workflow_id=task.workflow_id,
                task_id=task.task_id,
            ),
            json=task.result(max=self.MAX_RESULT_SIZE),
        )
