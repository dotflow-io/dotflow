"""Default subscribers for the internal event bus."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dotflow.core.events import StatusChanged
from dotflow.core.types.status import TypeStatus

if TYPE_CHECKING:
    from dotflow.abc.log import Log
    from dotflow.abc.metrics import Metrics
    from dotflow.abc.notify import Notify


class NotifySubscriber:
    """Forwards status changes to the configured notify provider."""

    def __init__(self, notify: Notify):
        self.notify = notify

    def __call__(self, event):
        if not isinstance(event, StatusChanged):
            return

        self.notify.hook_status_task(task=event.task)


class LogSubscriber:
    """Routes status changes to the configured log provider."""

    def __init__(self, log: Log):
        self.log = log

    def __call__(self, event):
        if not isinstance(event, StatusChanged):
            return

        if event.new == TypeStatus.FAILED:
            self.log.error(task=event.task)
        elif event.new == TypeStatus.RETRY:
            self.log.warning(task=event.task)
        else:
            self.log.info(task=event.task)


class MetricsSubscriber:
    """Updates task counters on status transitions."""

    def __init__(self, metrics: Metrics):
        self.metrics = metrics

    def __call__(self, event):
        if not isinstance(event, StatusChanged):
            return

        if event.new == TypeStatus.FAILED:
            self.metrics.task_failed(task=event.task)
        elif event.new == TypeStatus.RETRY:
            self.metrics.task_retried(task=event.task)
        elif event.new == TypeStatus.COMPLETED:
            self.metrics.task_completed(task=event.task)
