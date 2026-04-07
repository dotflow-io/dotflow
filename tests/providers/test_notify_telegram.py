"""Test NotifyTelegram"""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.abc.notify import Notify
from dotflow.core.types.status import TypeStatus
from dotflow.providers.notify_telegram import NotifyTelegram


class TestNotifyTelegram(unittest.TestCase):
    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = 0
        task.errors = []
        task.result.return_value = '{"foo": "bar"}'
        return task

    def test_instance(self):
        notify = NotifyTelegram(token="tok", chat_id=123)

        self.assertIsInstance(notify, Notify)

    def test_default_params(self):
        notify = NotifyTelegram(token="tok", chat_id=123)

        self.assertIsNone(notify.notification_type)
        self.assertFalse(notify.show_result)
        self.assertEqual(notify.timeout, 1.5)

    def test_skips_when_status_does_not_match(self):
        notify = NotifyTelegram(
            token="tok", chat_id=123, notification_type=TypeStatus.FAILED
        )
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_telegram.post") as mock_post:
            notify.hook_status_task(task=task)

        mock_post.assert_not_called()

    def test_sends_when_status_matches(self):
        notify = NotifyTelegram(
            token="tok", chat_id=123, notification_type=TypeStatus.COMPLETED
        )
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_telegram.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            notify.hook_status_task(task=task)

        mock_post.assert_called_once()

    def test_sends_when_no_filter(self):
        notify = NotifyTelegram(token="tok", chat_id=123)
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_telegram.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            notify.hook_status_task(task=task)

        mock_post.assert_called_once()

    def test_build_message_without_result(self):
        notify = NotifyTelegram(token="tok", chat_id=123)
        task = self._make_task()

        message = notify._build_message(task)

        self.assertIn("Completed", message)
        self.assertIn("wf-123", message)
        self.assertNotIn("json", message)

    def test_build_message_with_result(self):
        notify = NotifyTelegram(token="tok", chat_id=123, show_result=True)
        task = self._make_task()

        message = notify._build_message(task)

        self.assertIn("json", message)
        self.assertIn("foo", message)

    def test_build_message_with_error(self):
        notify = NotifyTelegram(token="tok", chat_id=123)
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "something broke"
        task.errors = [error]

        message = notify._build_message(task)

        self.assertIn("ValueError", message)
        self.assertIn("something broke", message)

    def test_logs_on_request_failure(self):
        notify = NotifyTelegram(token="tok", chat_id=123)
        task = self._make_task()

        with patch("dotflow.providers.notify_telegram.post") as mock_post:
            mock_post.side_effect = Exception("connection error")
            with patch("dotflow.providers.notify_telegram.logger") as mock_log:
                notify.hook_status_task(task=task)

        mock_log.error.assert_called_once()
