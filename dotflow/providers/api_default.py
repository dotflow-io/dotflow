"""Api Default

Default implementation that can persist dotflow executions in `dotflow-api`.

Note:
The current `dotflow-api` persists task rows only through the workflow creation
payload (`POST /workflows` with `WorkflowCreate.tasks`). The `dotflow` core
calls `create_workflow` before tasks are available and calls `create_task`
for each task added. For backward compatibility (and to avoid failures when
there is no tasks endpoint), this client:
1) Creates the workflow record (best-effort).
2) Keeps `create_task` as a safe no-op.
"""

from __future__ import annotations

import os
from typing import Any, Optional
from uuid import UUID

from dotflow.abc.api import Api
from dotflow.logging import logger

try:
    from requests import post  # type: ignore
except Exception:  # pragma: no cover
    post = None  # type: ignore


class ApiDefault(Api):
    """Default Api implementation (HTTP client)."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        user_token: Optional[str] = None,
        timeout: float = 5.0,
        enabled: Optional[bool] = None,
    ) -> None:
        env_enabled = os.getenv("DOTFLOW_API_ENABLED")
        self.base_url = (base_url or os.getenv("DOTFLOW_API_URL") or "").rstrip("/")
        self.user_token = user_token or os.getenv("DOTFLOW_USER_TOKEN")
        self.timeout = timeout

        if enabled is None:
            self.enabled = env_enabled is not None
        else:
            self.enabled = bool(enabled)

    def _is_ready(self) -> bool:
        if not self.enabled:
            return False
        if not post:
            logger.error("`requests` not available; cannot call dotflow-api.")
            return False
        if not self.base_url:
            logger.error("DOTFLOW_API_URL missing; cannot call dotflow-api.")
            return False
        if not self.user_token:
            logger.error("DOTFLOW_USER_TOKEN missing; cannot call dotflow-api.")
            return False
        return True

    @staticmethod
    def _callable_path(obj: Any) -> Optional[str]:
        if obj is None:
            return None
        if isinstance(obj, str):
            return obj
        module = getattr(obj, "__module__", None)
        name = getattr(obj, "__name__", None)
        if module and name:
            return f"{module}.{name}"
        return str(obj)

    def _workflow_to_payload(self, workflow: Any) -> dict[str, Any]:
        tasks_payload: list[dict[str, Any]] = []

        workflow_tasks = getattr(workflow, "tasks", None)
        if isinstance(workflow_tasks, (list, tuple)):
            for t in workflow_tasks:
                initial_context = getattr(
                    getattr(t, "initial_context", None),
                    "storage",
                    None,
                )
                tasks_payload.append(
                    {
                        "id": getattr(t, "task_id", None),
                        "step": self._callable_path(getattr(t, "step", None)),
                        "callback": self._callable_path(
                            getattr(t, "callback", None)
                        ),
                        "initial_context": initial_context,
                        "group_name": getattr(t, "group_name", None) or "default",
                    }
                )

        workflow_id = None
        if isinstance(workflow, UUID):
            workflow_id = str(workflow)
        elif isinstance(workflow, str):
            workflow_id = workflow

        payload: dict[str, Any] = {
            "tasks": tasks_payload,
            "execution_mode": "sequential",
            "keep_going": False,
        }

        if workflow_id:
            payload["id"] = workflow_id

        return payload

    def create_workflow(self, workflow: Any) -> None:
        """Create workflow record in `dotflow-api` (best-effort)."""
        if not self._is_ready():
            return None

        try:
            response = post(
                url=f"{self.base_url}/workflows",
                headers={
                    "Content-Type": "application/json",
                    "X-User-Token": str(self.user_token),
                },
                json=self._workflow_to_payload(workflow),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except Exception as error:
            logger.error("Failed to create workflow in dotflow-api: %s", str(error))

        return None

    def update_workflow(self, workflow: Any) -> None:
        """Update workflow record in `dotflow-api` (not implemented)."""
        return None

    def create_task(self, task: Any) -> None:
        """Create task record in `dotflow-api` (safe no-op).

        The current backend design persists tasks inside workflow creation.
        This method is intentionally a no-op to avoid breaking dotflow runs.
        """
        return None

    def update_task(self, task: Any) -> None:
        """Update task record in `dotflow-api` (not implemented)."""
        return None
