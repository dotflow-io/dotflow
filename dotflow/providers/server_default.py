"""ServerDefault - managed HTTP server provider."""

from __future__ import annotations

import os
from functools import wraps
from typing import Any

from requests import patch, post
from requests.exceptions import RequestException

from dotflow.abc.server import Server
from dotflow.logging import logger


def managed(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._managed:
            return
        return method(self, *args, **kwargs)

    return wrapper


class ServerDefault(Server):
    """Default Server provider with auto-detected managed mode.
    """

    MAX_RESULT_SIZE = 5_000_000
    TIMEOUT = 15.0

    ENDPOINT_WORKFLOWS = "/workflows"
    ENDPOINT_WORKFLOW = "/workflows/{workflow_id}"
    ENDPOINT_TASKS = "/workflows/{workflow_id}/tasks"
    ENDPOINT_TASK = "/workflows/{workflow_id}/tasks/{task_id}"

    def __init__(self) -> None:
        base_url = os.environ.get("SERVER_BASE_URL") or None
        user_token = os.environ.get("SERVER_USER_TOKEN") or None
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
            json={"id": str(workflow)},
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
        data = task.result(max=self.MAX_RESULT_SIZE)
        data["id"] = data.pop("task_id", task.task_id)
        self._post(
            self._base_url
            + self.ENDPOINT_TASKS.format(workflow_id=task.workflow_id),
            json=data,
        )

    @managed
    def update_task(self, task: Any) -> None:
        data = task.result(max=self.MAX_RESULT_SIZE)
        self._patch(
            self._base_url
            + self.ENDPOINT_TASK.format(
                workflow_id=task.workflow_id,
                task_id=task.task_id,
            ),
            json=data,
        )
