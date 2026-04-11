"""ServerDefault — no-op server provider."""

from __future__ import annotations

from typing import Any

from dotflow.abc.server import Server


class ServerDefault(Server):
    """Default Server implementation (no-op)."""

    def create_workflow(self, workflow: Any) -> None:
        pass

    def update_workflow(self, workflow: Any, status: str = "") -> None:
        pass

    def create_task(self, task: Any) -> None:
        pass

    def update_task(self, task: Any) -> None:
        pass
