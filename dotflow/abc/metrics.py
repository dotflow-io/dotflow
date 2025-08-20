"""Metrics ABC"""

from abc import ABC, abstractmethod


class Metrics(ABC):
    """Metrics
    """

    group = "metrics"

    @abstractmethod
    def post_status_count(self) -> None:
        pass
