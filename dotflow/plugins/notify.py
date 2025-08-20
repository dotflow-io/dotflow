"""Notify Hendler"""

from dotflow.abc.notify import Notify


class NotifyHandler(Notify):
    """Notify
    """

    def send(self, task_object) -> None:
        pass
