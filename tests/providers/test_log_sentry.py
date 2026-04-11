"""Test LogSentry"""

import sys
import unittest
from unittest.mock import MagicMock

from dotflow.abc.log import Log
from dotflow.core.types.status import TypeStatus

mock_sentry_sdk = MagicMock()
sys.modules["sentry_sdk"] = mock_sentry_sdk

from dotflow.providers.log_sentry import LogSentry  # noqa: E402, I001


class TestLogSentry(unittest.TestCase):
    def _make_sentry(self):
        log = LogSentry(dsn="https://test@sentry.io/1")
        log._sentry = MagicMock()
        return log

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = 0
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def _make_error(self):
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "broken"
        error.attempt = 1
        error.traceback = "Traceback: ValueError: broken"
        return error

    def test_instance(self):
        log = LogSentry(dsn="https://test@sentry.io/1")

        self.assertIsInstance(log, Log)

    def test_init_calls_sentry_init(self):
        sentry_mock = sys.modules["sentry_sdk"]
        sentry_mock.reset_mock()

        LogSentry(
            dsn="https://test@sentry.io/1",
            environment="staging",
            traces_sample_rate=0.5,
        )

        sentry_mock.init.assert_called_once_with(
            dsn="https://test@sentry.io/1",
            environment="staging",
            traces_sample_rate=0.5,
        )

    def test_error_captures_message(self):
        log = self._make_sentry()
        task = self._make_task(status=TypeStatus.FAILED)
        error = self._make_error()
        task.errors = [error]

        log.error(task=task)

        log._sentry.capture_message.assert_called_once()
        call_args = log._sentry.capture_message.call_args
        self.assertIn("Task 0 failed: broken", call_args[0][0])
        self.assertEqual(call_args[1]["level"], "error")
        self.assertEqual(call_args[1]["extras"]["workflow_id"], "wf-123")
        self.assertEqual(call_args[1]["extras"]["task_id"], "0")
        self.assertEqual(call_args[1]["extras"]["exception"], "ValueError")
        self.assertEqual(call_args[1]["extras"]["attempt"], 1)

    def test_error_no_task(self):
        log = self._make_sentry()

        log.error(workflow_id="wf-1")

        log._sentry.capture_message.assert_not_called()

    def test_error_no_errors(self):
        log = self._make_sentry()
        task = self._make_task(status=TypeStatus.FAILED)
        task.errors = []

        log.error(task=task)

        log._sentry.capture_message.assert_not_called()

    def test_info_adds_breadcrumb(self):
        log = self._make_sentry()
        task = self._make_task()

        log.info(task=task)

        log._sentry.add_breadcrumb.assert_called_once()
        call_args = log._sentry.add_breadcrumb.call_args
        self.assertEqual(call_args[1]["category"], "dotflow")
        self.assertEqual(call_args[1]["level"], "info")

    def test_info_no_task(self):
        log = self._make_sentry()

        log.info(workflow_id="wf-1")

        log._sentry.add_breadcrumb.assert_not_called()

    def test_warning_adds_breadcrumb(self):
        log = self._make_sentry()
        task = self._make_task(status=TypeStatus.RETRY)

        log.warning(task=task)

        log._sentry.add_breadcrumb.assert_called_once()
        call_args = log._sentry.add_breadcrumb.call_args
        self.assertEqual(call_args[1]["level"], "warning")

    def test_debug_is_noop(self):
        log = self._make_sentry()
        task = self._make_task()

        log.debug(task=task)

        log._sentry.add_breadcrumb.assert_not_called()
        log._sentry.capture_message.assert_not_called()

    def test_error_with_multiple_errors_uses_last(self):
        log = self._make_sentry()
        task = self._make_task(status=TypeStatus.FAILED)
        error1 = self._make_error()
        error1.message = "first"
        error2 = self._make_error()
        error2.message = "second"
        task.errors = [error1, error2]

        log.error(task=task)

        call_args = log._sentry.capture_message.call_args
        self.assertIn("second", call_args[0][0])
