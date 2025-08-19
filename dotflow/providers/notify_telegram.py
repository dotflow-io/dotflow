"""Notify Default"""

from json import dumps
from typing import Any, Optional

from requests import post

from dotflow.core.types.status import StatusTaskType
from dotflow.abc.notify import Notify
from dotflow.logging import logger


def get_symbol(value: str) -> str:
    status = {
        StatusTaskType.NOT_STARTED: "⚪",
        StatusTaskType.IN_PROGRESS: "🔵",
        StatusTaskType.COMPLETED: "✅",
        StatusTaskType.PAUSED: "◼️",
        StatusTaskType.RETRY: "❗",
        StatusTaskType.FAILED: "❌"
    }
    return status.get(value)


class NotifyTelegram(Notify):

    MESSAGE = "{symbol} {status}\n```json\n{task}```\n{workflow_id}-{task_id}"
    API_TELEGRAM = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(
        self,
        token: str,
        chat_id: int,
        notification_type: Optional[StatusTaskType] = None,
        timeout: int = 1.5
    ):
        self.token = token
        self.chat_id = chat_id
        self.notification_type = notification_type
        self.timeout = timeout

    def send(self, task: Any) -> None:
        if not self.notification_type or self.notification_type == task.status:
            data = {
                "chat_id": self.chat_id,
                "text": self._get_text(task=task),
                "parse_mode": "markdown",
            }
            try:
                response = post(
                    url=self.API_TELEGRAM.format(token=self.token),
                    headers={"Content-Type": "application/json"},
                    data=dumps(data),
                    timeout=self.timeout
                )
                response.raise_for_status()
            except Exception as error:
                logger.error(
                    "Internal problem sending notification on Telegram: %s",
                    str(error),
                )

    def _get_text(self, task: Any) -> str:
        return self.MESSAGE.format(
            symbol=get_symbol(task.status),
            status=task.status,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            task=task.result(max=4000),
        )
