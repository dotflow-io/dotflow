"""Test default subscribers."""

import unittest
from unittest.mock import Mock

from dotflow.core.events import StatusChanged
from dotflow.core.subscribers import (
    LogSubscriber,
    MetricsSubscriber,
    NotifySubscriber,
)
from dotflow.core.types.status import TypeStatus


def _event(new):
    return StatusChanged(task="task", old=TypeStatus.IN_PROGRESS, new=new)


class TestNotifySubscriber(unittest.TestCase):
    def test_calls_hook_status_task(self):
        notify = Mock()
        sub = NotifySubscriber(notify)

        sub(_event(TypeStatus.COMPLETED))

        notify.hook_status_task.assert_called_once_with(task="task")

    def test_ignores_unknown_event(self):
        notify = Mock()
        sub = NotifySubscriber(notify)

        sub("not a status change")

        notify.hook_status_task.assert_not_called()


class TestLogSubscriber(unittest.TestCase):
    def test_failed_uses_error(self):
        log = Mock()
        LogSubscriber(log)(_event(TypeStatus.FAILED))

        log.error.assert_called_once_with(task="task")
        log.warning.assert_not_called()
        log.info.assert_not_called()

    def test_retry_uses_warning(self):
        log = Mock()
        LogSubscriber(log)(_event(TypeStatus.RETRY))

        log.warning.assert_called_once_with(task="task")

    def test_completed_uses_info(self):
        log = Mock()
        LogSubscriber(log)(_event(TypeStatus.COMPLETED))

        log.info.assert_called_once_with(task="task")

    def test_other_status_uses_info(self):
        log = Mock()
        LogSubscriber(log)(_event(TypeStatus.IN_PROGRESS))

        log.info.assert_called_once_with(task="task")


class TestMetricsSubscriber(unittest.TestCase):
    def test_failed_calls_task_failed(self):
        metrics = Mock()
        MetricsSubscriber(metrics)(_event(TypeStatus.FAILED))

        metrics.task_failed.assert_called_once_with(task="task")

    def test_retry_calls_task_retried(self):
        metrics = Mock()
        MetricsSubscriber(metrics)(_event(TypeStatus.RETRY))

        metrics.task_retried.assert_called_once_with(task="task")

    def test_completed_calls_task_completed(self):
        metrics = Mock()
        MetricsSubscriber(metrics)(_event(TypeStatus.COMPLETED))

        metrics.task_completed.assert_called_once_with(task="task")

    def test_other_status_no_op(self):
        metrics = Mock()
        MetricsSubscriber(metrics)(_event(TypeStatus.IN_PROGRESS))

        metrics.task_failed.assert_not_called()
        metrics.task_retried.assert_not_called()
        metrics.task_completed.assert_not_called()
