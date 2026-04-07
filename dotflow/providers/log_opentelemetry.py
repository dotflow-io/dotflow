"""Log OpenTelemetry"""

from __future__ import annotations

from dotflow.abc.log import Log
from dotflow.core.exception import ModuleNotFound
from dotflow.core.types.status import TypeStatus


class LogOpenTelemetry(Log):
    """
    Import:
        You can import the **LogOpenTelemetry** class with:

            from dotflow.providers import LogOpenTelemetry

    Example:
        `class` dotflow.providers.log_opentelemetry.LogOpenTelemetry

            from dotflow import Config, DotFlow
            from dotflow.providers import LogOpenTelemetry

            config = Config(
                log=LogOpenTelemetry(service_name="my-pipeline"),
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

    def info(self, **kwargs) -> None:
        task = kwargs.get("task")
        if not task:
            return

        span = self._ensure_span(task)
        self._set_attributes(span, task)

        if task.status == TypeStatus.COMPLETED:
            span.set_status(self._status_ok)
            self._end_span(task)

    def error(self, **kwargs) -> None:
        task = kwargs.get("task")
        if not task:
            return

        span = self._get_span(task)
        if not span:
            return

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
        self._end_span(task)

    def warning(self, **kwargs) -> None:
        task = kwargs.get("task")
        if not task:
            return

        span = self._get_span(task)
        if not span:
            return

        span.add_event(
            "retry",
            attributes={
                "dotflow.task.status": str(task.status),
                "dotflow.task.retry_count": task.retry_count or 0,
            },
        )

    def debug(self, **kwargs) -> None:
        pass

    def _ensure_span(self, task):
        workflow_key = str(task.workflow_id)
        task_key = f"{workflow_key}:{task.task_id}"

        if workflow_key not in self._spans:
            span = self._tracer.start_span(name=f"workflow:{workflow_key}")
            span.set_attribute("dotflow.workflow_id", workflow_key)
            self._spans[workflow_key] = span

        if task_key not in self._spans:
            ctx = self._trace.set_span_in_context(self._spans[workflow_key])
            self._spans[task_key] = self._tracer.start_span(
                name=f"task:{task.task_id}", context=ctx
            )

        return self._spans[task_key]

    def _get_span(self, task):
        task_key = f"{task.workflow_id}:{task.task_id}"
        return self._spans.get(task_key)

    def _end_span(self, task):
        task_key = f"{task.workflow_id}:{task.task_id}"
        span = self._spans.pop(task_key, None)
        if span:
            span.end()

    def _set_attributes(self, span, task):
        span.set_attribute("dotflow.workflow_id", str(task.workflow_id))
        span.set_attribute("dotflow.task_id", str(task.task_id))
        span.set_attribute("dotflow.task.status", str(task.status))

        if task.duration:
            span.set_attribute("dotflow.task.duration", task.duration)
        if task.retry_count:
            span.set_attribute("dotflow.task.retry_count", task.retry_count)
