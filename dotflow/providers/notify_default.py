"""Notify Default"""

from typing import Any

from dotflow.abc.notify import Notify


class NotifyDefault(Notify):

    def hook_status_task(self, task: Any) -> None:
        pass
