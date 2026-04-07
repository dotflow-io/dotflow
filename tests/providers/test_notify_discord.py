"""Test NotifyDiscord"""

import unittest
from unittest.mock import MagicMock, patch

from dotflow.abc.notify import Notify
from dotflow.core.types.status import TypeStatus
from dotflow.providers.notify_discord import NotifyDiscord


class TestNotifyDiscord(unittest.TestCase):
    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = 0
        task.errors = []
        task.result.return_value = '{"foo": "bar"}'
        return task

    def test_instance(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )

        self.assertIsInstance(notify, Notify)

    def test_default_params(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )

        self.assertIsNone(notify.notification_type)
        self.assertFalse(notify.show_result)
        self.assertEqual(notify.timeout, 1.5)

    def test_skips_when_status_does_not_match(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test",
            notification_type=TypeStatus.FAILED,
        )
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_discord.post") as mock_post:
            notify.hook_status_task(task=task)

        mock_post.assert_not_called()

    def test_sends_when_status_matches(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test",
            notification_type=TypeStatus.COMPLETED,
        )
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_discord.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            notify.hook_status_task(task=task)

        mock_post.assert_called_once()

    def test_sends_when_no_filter(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )
        task = self._make_task(status=TypeStatus.COMPLETED)

        with patch("dotflow.providers.notify_discord.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            notify.hook_status_task(task=task)

        mock_post.assert_called_once()

    def test_build_embed_basic(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )
        task = self._make_task()

        embed = notify._build_embed(task)

        self.assertIn("Completed", embed["title"])
        self.assertEqual(embed["color"], 0x4CAF50)
        self.assertIn("wf-123", embed["description"])

    def test_build_embed_without_result(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )
        task = self._make_task()

        embed = notify._build_embed(task)

        field_names = [f["name"] for f in embed["fields"]]
        self.assertNotIn("Result", field_names)

    def test_build_embed_with_result(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test",
            show_result=True,
        )
        task = self._make_task()

        embed = notify._build_embed(task)

        field_names = [f["name"] for f in embed["fields"]]
        self.assertIn("Result", field_names)

    def test_build_embed_with_error(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "something broke"
        task.errors = [error]

        embed = notify._build_embed(task)

        field_names = [f["name"] for f in embed["fields"]]
        self.assertIn("Error", field_names)

    def test_color_mapping(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )

        self.assertEqual(notify.COLORS[TypeStatus.COMPLETED], 0x4CAF50)
        self.assertEqual(notify.COLORS[TypeStatus.FAILED], 0xF44336)
        self.assertEqual(notify.COLORS[TypeStatus.RETRY], 0xFF9800)

    def test_logs_on_request_failure(self):
        notify = NotifyDiscord(
            webhook_url="https://discord.com/api/webhooks/test"
        )
        task = self._make_task()

        with patch("dotflow.providers.notify_discord.post") as mock_post:
            mock_post.side_effect = Exception("connection error")
            with patch("dotflow.providers.notify_discord.logger") as mock_log:
                notify.hook_status_task(task=task)

        mock_log.error.assert_called_once()
