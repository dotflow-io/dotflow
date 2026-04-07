"""Tracer Sentry"""

from __future__ import annotations

from typing import Any

from dotflow.abc.tracer import Tracer
from dotflow.core.exception import ModuleNotFound


class TracerSentry(Tracer):
    """
    Import:
        You can import the **TracerSentry** class with:

            from dotflow.providers import TracerSentry

    Example:
        `class` dotflow.providers.tracer_sentry.TracerSentry

            from dotflow import Config, DotFlow
            from dotflow.providers import TracerSentry

            config = Config(
                tracer=TracerSentry(),
            )

            workflow = DotFlow(config=config)

    Args:
        dsn (str): Sentry DSN for the project. If None, uses the SDK
            already initialized by LogSentry or manually.
        environment (str): Environment tag sent to Sentry.
            Defaults to None.
        traces_sample_rate (float): Sample rate for performance traces (0.0 to 1.0).
            Defaults to 1.0.
    """

    def __init__(
        self,
        dsn: str | None = None,
        environment: str | None = None,
        traces_sample_rate: float = 1.0,
    ) -> None:
        try:
            import sentry_sdk
        except ImportError as err:
            raise ModuleNotFound(
                module="sentry-sdk", library="dotflow[sentry]"
            ) from err

        if dsn:
            sentry_sdk.init(
                dsn=dsn,
                environment=environment,
                traces_sample_rate=traces_sample_rate,
            )

        self._sentry = sentry_sdk
        self._transactions: dict[str, Any] = {}
        self._spans: dict[str, Any] = {}

    def start_workflow(self, workflow_id: Any, **kwargs) -> None:
        key = str(workflow_id)
        transaction = self._sentry.start_transaction(
            op="workflow",
            name=f"workflow:{key}",
        )
        transaction.set_tag("dotflow.workflow_id", key)

        for k, v in kwargs.items():
            transaction.set_tag(f"dotflow.{k}", str(v))

        self._transactions[key] = transaction

    def end_workflow(self, workflow_id: Any, **kwargs) -> None:
        key = str(workflow_id)
        transaction = self._transactions.pop(key, None)
        if not transaction:
            return

        failed = kwargs.get("failed", False)
        transaction.set_status("internal_error" if failed else "ok")

        if "duration" in kwargs:
            transaction.set_data("dotflow.duration", kwargs["duration"])

        transaction.finish()

    def start_task(self, task: Any) -> None:
        workflow_key = str(task.workflow_id)
        task_key = f"{workflow_key}:{task.task_id}"

        transaction = self._transactions.get(workflow_key)
        if not transaction:
            return

        span = transaction.start_child(
            op="task",
            description=f"task:{task.task_id}",
        )
        span.set_tag("dotflow.workflow_id", workflow_key)
        span.set_tag("dotflow.task_id", str(task.task_id))
        self._spans[task_key] = span

    def end_task(self, task: Any) -> None:
        task_key = f"{task.workflow_id}:{task.task_id}"
        span = self._spans.pop(task_key, None)
        if not span:
            return

        span.set_tag("dotflow.task.status", str(task.status))

        if task.duration is not None:
            span.set_data("dotflow.task.duration", task.duration)
        if task.retry_count:
            span.set_data("dotflow.task.retry_count", task.retry_count)

        if task.errors:
            last_error = task.errors[-1]
            span.set_data("dotflow.task.exception", str(last_error.exception))
            span.set_status("internal_error")
        else:
            span.set_status("ok")

        span.finish()
