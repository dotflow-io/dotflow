"""Metrics Default"""

from typing import Any

from dotflow.abc.metrics import Metrics


class MetricsDefault(Metrics):
    def workflow_started(self, workflow_id: Any, **kwargs) -> None:
        pass

    def workflow_completed(self, workflow_id: Any, duration: float) -> None:
        pass

    def workflow_failed(self, workflow_id: Any, duration: float) -> None:
        pass

    def task_completed(self, task: Any) -> None:
        pass

    def task_failed(self, task: Any) -> None:
        pass

    def task_retried(self, task: Any) -> None:
        pass
