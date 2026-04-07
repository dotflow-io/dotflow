"""Log Sentry"""

from __future__ import annotations

from dotflow.abc.log import Log
from dotflow.core.exception import ModuleNotFound


class LogSentry(Log):
    """
    Import:
        You can import the **LogSentry** class with:

            from dotflow.providers import LogSentry

    Example:
        `class` dotflow.providers.log_sentry.LogSentry

            from dotflow import Config, DotFlow
            from dotflow.providers import LogSentry

            config = Config(
                log=LogSentry(
                    dsn="https://xxx@sentry.io/123",
                    environment="production",
                ),
            )

            workflow = DotFlow(config=config)

    Args:
        dsn (str): Sentry DSN for the project.
        environment (str): Environment tag sent to Sentry.
            Defaults to None.
        traces_sample_rate (float): Sample rate for performance traces (0.0 to 1.0).
            Defaults to 0.0.
    """

    def __init__(
        self,
        dsn: str,
        environment: str | None = None,
        traces_sample_rate: float = 0.0,
    ) -> None:
        try:
            import sentry_sdk
        except ImportError as err:
            raise ModuleNotFound(
                module="sentry-sdk", library="dotflow[sentry]"
            ) from err

        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            traces_sample_rate=traces_sample_rate,
        )
        self._sentry = sentry_sdk

    def info(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._sentry.add_breadcrumb(
                category="dotflow",
                message=f"task:{task.task_id} {task.status}",
                level="info",
            )

    def error(self, **kwargs) -> None:
        task = kwargs.get("task")
        if not task or not task.errors:
            return

        last_error = task.errors[-1]
        self._sentry.capture_message(
            f"Task {task.task_id} failed: {last_error.message}",
            level="error",
            extras={
                "workflow_id": str(task.workflow_id),
                "task_id": str(task.task_id),
                "exception": str(last_error.exception),
                "attempt": last_error.attempt,
                "traceback": last_error.traceback,
            },
        )

    def warning(self, **kwargs) -> None:
        task = kwargs.get("task")
        if task:
            self._sentry.add_breadcrumb(
                category="dotflow",
                message=f"task:{task.task_id} {task.status}",
                level="warning",
            )

    def debug(self, **kwargs) -> None:
        pass
