"""Metrics OpenTelemetry"""

from __future__ import annotations

from typing import Any

from dotflow.abc.metrics import Metrics
from dotflow.core.exception import ModuleNotFound


class MetricsOpenTelemetry(Metrics):
    """
    Import:
        You can import the **MetricsOpenTelemetry** class with:

            from dotflow.providers import MetricsOpenTelemetry

    Example:
        `class` dotflow.providers.metrics_opentelemetry.MetricsOpenTelemetry

            from dotflow import Config, DotFlow
            from dotflow.providers import MetricsOpenTelemetry

            config = Config(
                metrics=MetricsOpenTelemetry(service_name="my-pipeline"),
            )

            workflow = DotFlow(config=config)

    Args:
        service_name (str): The service name used in the OpenTelemetry meter.
    """

    def __init__(self, service_name: str = "dotflow") -> None:
        try:
            from opentelemetry import metrics
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.resources import Resource
        except ImportError as err:
            raise ModuleNotFound(
                module="opentelemetry", library="dotflow[otel]"
            ) from err

        resource = Resource.create({"service.name": service_name})
        provider = MeterProvider(resource=resource)
        metrics.set_meter_provider(provider)

        meter = metrics.get_meter("dotflow")

        self._workflow_total = meter.create_counter(
            name="dotflow_workflow_total",
            description="Total workflows executed",
        )
        self._workflow_duration = meter.create_histogram(
            name="dotflow_workflow_duration_seconds",
            description="Workflow execution duration in seconds",
            unit="s",
        )
        self._task_total = meter.create_counter(
            name="dotflow_task_total",
            description="Total tasks executed by status",
        )
        self._task_duration = meter.create_histogram(
            name="dotflow_task_duration_seconds",
            description="Task execution duration in seconds",
            unit="s",
        )
        self._task_retry_total = meter.create_counter(
            name="dotflow_task_retry_total",
            description="Total task retries",
        )

    def workflow_started(self, workflow_id: Any, **kwargs) -> None:
        self._workflow_total.add(1, {"status": "started"})

    def workflow_completed(self, workflow_id: Any, duration: float) -> None:
        self._workflow_total.add(1, {"status": "completed"})
        self._workflow_duration.record(duration, {"status": "completed"})

    def workflow_failed(self, workflow_id: Any, duration: float) -> None:
        self._workflow_total.add(1, {"status": "failed"})
        self._workflow_duration.record(duration, {"status": "failed"})

    def task_completed(self, task: Any) -> None:
        self._task_total.add(1, {"status": "completed"})
        if task.duration is not None:
            self._task_duration.record(task.duration, {"status": "completed"})

    def task_failed(self, task: Any) -> None:
        self._task_total.add(1, {"status": "failed"})
        if task.duration is not None:
            self._task_duration.record(task.duration, {"status": "failed"})

    def task_retried(self, task: Any) -> None:
        self._task_retry_total.add(1)
