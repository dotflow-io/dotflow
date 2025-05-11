"""Notify Default"""

from typing import Any

from dotflow.abc.notify import Notify


class NotifyDefault(Notify):

    def send(self, task: Any) -> None:
        pass
