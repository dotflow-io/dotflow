"""Notify Telegram"""

from __future__ import annotations

from json import dumps
from typing import Any

from requests import post

from dotflow.abc.notify import Notify
from dotflow.core.types.status import TypeStatus
from dotflow.logging import logger


class NotifyTelegram(Notify):
    """
    Import:
        You can import the **NotifyTelegram** class with:

            from dotflow.providers import NotifyTelegram

    Example:
        `class` dotflow.providers.notify_telegram.NotifyTelegram

            from dotflow import Config, DotFlow
            from dotflow.providers import NotifyTelegram
            from dotflow.core.types.status import TypeStatus

            config = Config(
                notify=NotifyTelegram(
                    token="YOUR_BOT_TOKEN",
                    chat_id=123456789,
                    notification_type=TypeStatus.FAILED,
                )
            )

            workflow = DotFlow(config=config)

    Args:
        token (str): Telegram bot token from BotFather.

        chat_id (int): Telegram chat ID to send messages to.

        notification_type (Optional[TypeStatus]): Filter notifications
            by task status. If None, all statuses are notified.

        show_result (bool): Include task result in the notification.
            Defaults to False.

        timeout (float): Request timeout in seconds.
    """

    API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(
        self,
        token: str,
        chat_id: int,
        notification_type: TypeStatus | None = None,
        show_result: bool = False,
        timeout: float = 1.5,
    ):
        self.token = token
        self.chat_id = chat_id
        self.notification_type = notification_type
        self.show_result = show_result
        self.timeout = timeout

    def hook_status_task(self, task: Any) -> None:
        if self.notification_type and self.notification_type != task.status:
            return

        try:
            response = post(
                url=self.API_URL.format(token=self.token),
                headers={"Content-Type": "application/json"},
                data=dumps(
                    {
                        "chat_id": self.chat_id,
                        "text": self._build_message(task),
                        "parse_mode": "markdown",
                    }
                ),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except Exception as error:
            logger.error(
                "Internal problem sending notification on Telegram: %s",
                str(error),
            )

    def _build_message(self, task: Any) -> str:
        symbol = TypeStatus.get_symbol(task.status)
        header = f"{symbol} {task.status}"
        footer = f"`{task.workflow_id}` — Task {task.task_id}"

        parts = [header]

        if self.show_result:
            parts.append(f"```json\n{task.result(max=4000)}```")

        if task.status == TypeStatus.FAILED and task.errors:
            last_error = task.errors[-1]
            parts.append(f"`{last_error.exception}`: {last_error.message}")

        parts.append(footer)

        return "\n".join(parts)
