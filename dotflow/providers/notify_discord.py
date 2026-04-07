"""Notify Discord"""

from json import dumps
from typing import Any, Optional

from requests import post

from dotflow.core.types.status import TypeStatus
from dotflow.abc.notify import Notify
from dotflow.logging import logger


class NotifyDiscord(Notify):

    def __init__(
        self,
        webhook_url: str,
        notification_type: Optional[str] = None,
        timeout: int = 2.0
    ):
        self.webhook_url = webhook_url
        self.notification_type = notification_type
        self.timeout = timeout

    def send(self, task: Any) -> None:
        if not self.notification_type or self.notification_type == task.status:
            data = {
                "embeds": [
                    {
                        "title": f"{TypeStatus.get_symbol(task.status)} {task.status}",
                        "description": f"```json\n{task.result(max=2000)}```",
                        "fields": [
                            {"name": "Workflow ID", "value": str(task.workflow_id), "inline": True},
                            {"name": "Task ID", "value": str(task.task_id), "inline": True},
                        ],
                        "color": self._get_color(task.status)
                    }
                ]
            }
            try:
                response = post(
                    url=self.webhook_url,
                    headers={"Content-Type": "application/json"},
                    data=dumps(data),
                    timeout=self.timeout
                )
                response.raise_for_status()
            except Exception as error:
                logger.error(
                    "Internal problem sending notification on Discord: %s",
                    str(error),
                )

    def _get_color(self, status: str) -> int:
        if status == TypeStatus.COMPLETED:
            return 0x00FF00  # Green
        if status == TypeStatus.FAILED:
            return 0xFF0000  # Red
        if status == TypeStatus.IN_PROGRESS:
            return 0x3498DB  # Blue
        return 0x95A5A6  # Gray
