"""Metrics ABC"""

from abc import ABC, abstractmethod


class Metrics(ABC):
    """Metrics
    """

    group = "metrics"  # Do not remove

    def __init__(self, *_args, **_kwargs):
        """Init not implemented."""
        self.client = None

    @abstractmethod
    def workflow_count(self, workflow_objetc) -> None:
        pass

    @abstractmethod
    def task_count(self, task_objetc) -> None:
        pass
