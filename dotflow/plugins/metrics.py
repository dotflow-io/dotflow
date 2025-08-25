"""Metrics Handler"""

from dotflow.abc.metrics import Metrics
from dotflow.core.decorators.tools import _threading
from dotflow.providers.otel.metrics import client


class MetricsHandler(Metrics):
    """Metrics
    """

    def __init__(self):
        self.client = client
        self.task_counter = self.client.create_counter(
            name="dotflow_task",
            unit="1"
        )
        self.workflow_counter = self.client.create_counter(
            name="dotflow_workflow",
            unit="1"
        )

    @_threading
    def workflow_count(self, workflow_objet) -> None:
        self.workflow_counter.add(
            amount=1,
            attributes={
                "workflow_id": str(workflow_objet.workflow_id)}
            )

    @_threading
    def task_count(self, task_objetc) -> None:
        self.task_counter.add(
            amount=1,
            attributes={
                "task_id": task_objetc.task_id,
                "workflow_id": str(task_objetc.workflow_id)}
            )
