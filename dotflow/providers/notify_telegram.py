"""Notify Default"""

from json import dumps
from typing import Dict

from requests import post

from dotflow.abc.notify import Notify
from dotflow.logging import logger


class NotifyTelegram(Notify):

    def __init__(self, token: str, chat_id: int):
        self.token = token
        self.chat_id = chat_id

    def send(self, task: Dict[str, any]) -> None:
        try:
            response = post(
                url=f"https://api.telegram.org/bot{self.token}/sendMessage",
                headers={"Content-Type": "application/json"},
                data=dumps(
                    {
                        "chat_id": self.chat_id,
                        "text": f"```json\n{task}```",
                        "parse_mode": "markdown",
                    }
                ),
            )
            response.raise_for_status()
        except Exception as error:
            logger.error(
                "Internal problem sending notification on Telegram: %s",
                str(error),
            )
