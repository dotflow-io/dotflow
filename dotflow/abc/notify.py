"""Notify ABC"""

from abc import ABC, abstractmethod


class Notify(ABC):
    """Notify"""

    group = "notify"  # Do not remove

    def __init__(self, *_args, **_kwargs):
        """Init not implemented."""
        self.client = None

    @abstractmethod
    def send(self, task_object) -> None:
        """Send"""
