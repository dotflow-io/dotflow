"""Tracer OpenTelemetry"""

from __future__ import annotations

from typing import Any

from dotflow.abc.tracer import Tracer
from dotflow.core.exception import ModuleNotFound
from dotflow.core.types.status import TypeStatus


class TracerOpenTelemetry(Tracer):
    """
    Import:
        You can import the **TracerOpenTelemetry** class with:

            from dotflow.providers import TracerOpenTelemetry

    Example:
        `class` dotflow.providers.tracer_opentelemetry.TracerOpenTelemetry

            from dotflow import Config, DotFlow
            from dotflow.providers import TracerOpenTelemetry

            config = Config(
                tracer=TracerOpenTelemetry(service_name="my-pipeline"),
            )

            workflow = DotFlow(config=config)

    Args:
        service_name (str): The service name used in the OpenTelemetry tracer.
    """

    def __init__(self, service_name: str = "dotflow") -> None:
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.trace import StatusCode
        except ImportError as err:
            raise ModuleNotFound(
                module="opentelemetry", library="dotflow[otel]"
            ) from err

        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

        self._trace = trace
        self._tracer = trace.get_tracer("dotflow")
        self._status_ok = StatusCode.OK
        self._status_error = StatusCode.ERROR
        self._spans: dict = {}

    def start_workflow(self, workflow_id: Any, **kwargs) -> None:
        key = str(workflow_id)
        if key not in self._spans:
            span = self._tracer.start_span(name=f"workflow:{key}")
            span.set_attribute("dotflow.workflow_id", key)
            for k, v in kwargs.items():
                span.set_attribute(f"dotflow.{k}", str(v))
            self._spans[key] = span

    def end_workflow(self, workflow_id: Any, **kwargs) -> None:
        key = str(workflow_id)
        span = self._spans.pop(key, None)
        if not span:
            return

        failed = kwargs.get("failed", False)
        if failed:
            span.set_status(self._status_error, "workflow failed")
        else:
            span.set_status(self._status_ok)

        if "duration" in kwargs:
            span.set_attribute("dotflow.duration", kwargs["duration"])

        span.end()

    def start_task(self, task: Any) -> None:
        workflow_key = str(task.workflow_id)
        task_key = f"{workflow_key}:{task.task_id}"

        workflow_span = self._spans.get(workflow_key)
        if workflow_span:
            ctx = self._trace.set_span_in_context(workflow_span)
        else:
            ctx = None

        span = self._tracer.start_span(
            name=f"task:{task.task_id}", context=ctx
        )
        span.set_attribute("dotflow.workflow_id", workflow_key)
        span.set_attribute("dotflow.task_id", str(task.task_id))
        self._spans[task_key] = span

    def end_task(self, task: Any) -> None:
        task_key = f"{task.workflow_id}:{task.task_id}"
        span = self._spans.pop(task_key, None)
        if not span:
            return

        span.set_attribute("dotflow.task.status", str(task.status))

        if task.duration:
            span.set_attribute("dotflow.task.duration", task.duration)
        if task.retry_count:
            span.set_attribute("dotflow.task.retry_count", task.retry_count)

        if task.status == TypeStatus.FAILED:
            if task.errors:
                last_error = task.errors[-1]
                span.add_event(
                    "exception",
                    attributes={
                        "exception.type": str(last_error.exception),
                        "exception.message": str(last_error.message),
                    },
                )
            span.set_status(self._status_error, str(task.status))
        else:
            span.set_status(self._status_ok)

        span.end()
