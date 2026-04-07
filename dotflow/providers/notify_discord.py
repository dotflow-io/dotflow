"""Notify Discord"""

from __future__ import annotations

from json import dumps
from typing import Any

from requests import post

from dotflow.abc.notify import Notify
from dotflow.core.types.status import TypeStatus
from dotflow.logging import logger


class NotifyDiscord(Notify):
    """
    Import:
        You can import the **NotifyDiscord** class with:

            from dotflow.providers import NotifyDiscord

    Example:
        `class` dotflow.providers.notify_discord.NotifyDiscord

            from dotflow import Config, DotFlow
            from dotflow.providers import NotifyDiscord
            from dotflow.core.types.status import TypeStatus

            config = Config(
                notify=NotifyDiscord(
                    webhook_url="https://discord.com/api/webhooks/...",
                    notification_type=TypeStatus.FAILED,
                )
            )

            workflow = DotFlow(config=config)

    Args:
        webhook_url (str): Discord webhook URL.

        notification_type (Optional[TypeStatus]): Filter notifications
            by task status. If None, all statuses are notified.

        show_result (bool): Include task result in the notification.
            Defaults to False.

        timeout (float): Request timeout in seconds.
    """

    COLORS = {
        TypeStatus.COMPLETED: 0x4CAF50,
        TypeStatus.FAILED: 0xF44336,
        TypeStatus.RETRY: 0xFF9800,
        TypeStatus.IN_PROGRESS: 0x2196F3,
        TypeStatus.NOT_STARTED: 0x9E9E9E,
        TypeStatus.PAUSED: 0x607D8B,
    }

    def __init__(
        self,
        webhook_url: str,
        notification_type: TypeStatus | None = None,
        show_result: bool = False,
        timeout: float = 1.5,
    ):
        self.webhook_url = webhook_url
        self.notification_type = notification_type
        self.show_result = show_result
        self.timeout = timeout

    def hook_status_task(self, task: Any) -> None:
        if self.notification_type and self.notification_type != task.status:
            return

        try:
            response = post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=dumps({"embeds": [self._build_embed(task)]}),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except Exception as error:
            logger.error(
                "Internal problem sending notification on Discord: %s",
                str(error),
            )

    def _build_embed(self, task: Any) -> dict:
        embed = {
            "title": f"{TypeStatus.get_symbol(task.status)} {task.status}",
            "color": self.COLORS.get(task.status, 0x9E9E9E),
            "description": f"`{task.workflow_id}` — Task {task.task_id}",
            "fields": [],
        }

        if self.show_result:
            embed["fields"].append(
                {
                    "name": "Result",
                    "value": f"```json\n{task.result(max=1024)}```",
                }
            )

        if task.status == TypeStatus.FAILED and task.errors:
            last_error = (
                task.errors[-1]
                if isinstance(task.errors, list)
                else task.errors
            )
            embed["fields"].append(
                {
                    "name": "Error",
                    "value": f"`{last_error.exception}`: {last_error.message}"[
                        :1024
                    ],
                }
            )

        return embed
