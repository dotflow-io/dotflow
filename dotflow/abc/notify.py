"""Notify ABC"""

from abc import ABC, abstractmethod


class Notify(ABC):
    """Notify"""

    group = "notify"

    @abstractmethod
    def send(self, task_object) -> None:
        """Send"""

    def send_on_status_in_queue(self):
        pass

    def send_on_status_in_progress(self):
        pass

    def send_on_status_completed(self):
        pass

    def send_on_status_paused(self):
        pass

    def send_on_status_retry(self):
        pass

    def send_on_status_failed(self):
        pass
