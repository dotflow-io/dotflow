"""Test ServerDefault provider"""

import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from dotflow.providers.server_default import ServerDefault


class TestServerDefaultInit(unittest.TestCase):
    def test_defaults(self):
        server = ServerDefault()
        self.assertEqual(server.base_url, "")
        self.assertEqual(server.user_token, "")
        self.assertEqual(server.timeout, 5.0)
        self.assertFalse(server.enabled)

    def test_with_args(self):
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token-123",
        )
        self.assertEqual(
            server.base_url,
            "http://localhost:8000/api/v1",
        )
        self.assertEqual(server.user_token, "token-123")
        self.assertTrue(server.enabled)

    def test_strips_trailing_slash(self):
        server = ServerDefault(
            base_url="http://localhost:8000/",
            user_token="token",
        )
        self.assertEqual(server.base_url, "http://localhost:8000")

    def test_enabled_requires_both(self):
        s1 = ServerDefault(base_url="http://x")
        self.assertFalse(s1.enabled)

        s2 = ServerDefault(user_token="t")
        self.assertFalse(s2.enabled)

        s3 = ServerDefault(base_url="http://x", user_token="t")
        self.assertTrue(s3.enabled)


class TestServerDefaultCreateWorkflow(unittest.TestCase):
    def test_skips_when_disabled(self):
        server = ServerDefault()
        server.create_workflow(workflow=uuid4())

    @patch("dotflow.providers.server_default.http_post")
    def test_posts_workflow(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201)
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        uid = uuid4()
        server.create_workflow(workflow=uid)
        mock_post.assert_called_once()
        payload = mock_post.call_args[1]["json"]
        self.assertEqual(payload["id"], str(uid))

    @patch(
        "dotflow.providers.server_default.http_post",
        side_effect=Exception("fail"),
    )
    def test_handles_error(self, _mock_post):
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        server.create_workflow(workflow=uuid4())


class TestServerDefaultCreateTask(unittest.TestCase):
    def test_skips_when_disabled(self):
        server = ServerDefault()
        server.create_task(task=MagicMock())

    @patch("dotflow.providers.server_default.http_post")
    def test_posts_task(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201)
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        task = MagicMock()
        task.workflow_id = uuid4()
        task.task_id = 0
        task.step = "mod.step_fn"
        task.callback = "mod.callback_fn"
        task.initial_context.storage = None
        task.group_name = "default"
        server.create_task(task=task)
        mock_post.assert_called_once()


class TestServerDefaultUpdateWorkflow(unittest.TestCase):
    def test_skips_when_disabled(self):
        server = ServerDefault()
        server.update_workflow(workflow=uuid4())

    @patch("dotflow.providers.server_default.http_patch")
    def test_patches_workflow(self, mock_patch):
        mock_patch.return_value = MagicMock(status_code=200)
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        uid = uuid4()
        server.update_workflow(workflow=uid, status="Completed")
        mock_patch.assert_called_once()
        payload = mock_patch.call_args[1]["json"]
        self.assertEqual(payload["status"], "Completed")


class TestServerDefaultUpdateTask(unittest.TestCase):
    def test_skips_when_disabled(self):
        server = ServerDefault()
        server.update_task(task=MagicMock())

    @patch("dotflow.providers.server_default.http_patch")
    def test_patches_task(self, mock_patch):
        mock_patch.return_value = MagicMock(status_code=200)
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        task = MagicMock()
        task.task_id = 1
        task.result.return_value = {"status": "Completed"}
        server.update_task(task=task)
        mock_patch.assert_called_once()

    @patch("dotflow.providers.server_default.http_patch")
    def test_sends_result(self, mock_patch):
        mock_patch.return_value = MagicMock(status_code=200)
        server = ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="token",
        )
        task = MagicMock()
        task.task_id = 5
        task.result.return_value = {"status": "Failed"}
        server.update_task(task=task)
        mock_patch.assert_called_once()
        payload = mock_patch.call_args[1]["json"]
        self.assertEqual(payload["status"], "Failed")
