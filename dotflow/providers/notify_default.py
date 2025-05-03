"""Notify Default"""

from typing import Dict

from dotflow.abc.notify import Notify


class NotifyDefault(Notify):

    def send(self, task: Dict[str, any]) -> None:
        pass
