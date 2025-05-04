"""Notify Default"""

from json import dumps
from typing import Any, Optional

from requests import post

from dotflow.core.types.status import TypeStatus
from dotflow.abc.notify import Notify
from dotflow.logging import logger

API_TELEGRAM = "https://api.telegram.org/bot{token}/sendMessage"


class NotifyTelegram(Notify):

    def __init__(
        self, token: str, chat_id: int, notification_type: Optional[TypeStatus] = None
    ):
        self.token = token
        self.chat_id = chat_id
        self.notification_type = notification_type

    def send(self, task: Any) -> None:
        if not self.notification_type or self.notification_type == task.status:
            data = dumps(
                {
                    "chat_id": self.chat_id,
                    "text": self._get_text(task=task),
                    "parse_mode": "markdown",
                }
            )
            try:
                response = post(
                    url=API_TELEGRAM.format(token=self.token),
                    headers={"Content-Type": "application/json"},
                    timeout=5,
                    data=data,
                )
                response.raise_for_status()
                return None
            except Exception as error:
                logger.error(
                    "Internal problem sending notification on Telegram: %s",
                    str(error),
                )

    def _get_text(self, task: Any) -> str:
        text = "{symbol} {status}\n```json\n{task}```\n{workflow_id}-{task_id}"

        return text.format(
            symbol=TypeStatus.get_symbol(task.status),
            status=task.status,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            task=task.result(),
        )
