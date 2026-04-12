import unittest
from unittest.mock import MagicMock, patch

from requests.exceptions import RequestException

from dotflow.providers.server_api import ServerAPI


class TestServerAPI(unittest.TestCase):

    def setUp(self):
        self.server = ServerAPI(
            base_url="https://example.com/api/v1/",
            user_token="tok-123",
        )

    def test_strips_trailing_slash_from_base_url(self):
        self.assertEqual(self.server._base_url, "https://example.com/api/v1")

    def test_headers_include_bearer_token(self):
        self.assertEqual(
            self.server._headers,
            {
                "Authorization": "Bearer tok-123",
                "Content-Type": "application/json",
            },
        )

    @patch("dotflow.providers.server_api.post")
    def test_create_workflow_posts_id(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201)
        self.server.create_workflow(workflow="wf-1")
        mock_post.assert_called_once_with(
            "https://example.com/api/v1/workflows",
            json={"id": "wf-1"},
            headers=self.server._headers,
            timeout=15.0,
        )

    @patch("dotflow.providers.server_api.patch")
    def test_update_workflow_patches_status(self, mock_patch):
        mock_patch.return_value = MagicMock(status_code=200)
        self.server.update_workflow(workflow="wf-1", status="Completed")
        mock_patch.assert_called_once_with(
            "https://example.com/api/v1/workflows/wf-1",
            json={"status": "Completed"},
            headers=self.server._headers,
            timeout=15.0,
        )

    @patch("dotflow.providers.server_api.post")
    def test_create_task_posts_to_task_list(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201)
        task = MagicMock()
        task.workflow_id = "wf-1"
        task.task_id = 42
        task.result.return_value = {"task_id": 42, "status": "Not started"}

        self.server.create_task(task=task)

        mock_post.assert_called_once_with(
            "https://example.com/api/v1/workflows/wf-1/tasks",
            json={"id": 42, "status": "Not started"},
            headers=self.server._headers,
            timeout=15.0,
        )

    @patch("dotflow.providers.server_api.patch")
    def test_update_task_patches_status(self, mock_patch):
        mock_patch.return_value = MagicMock(status_code=200)
        task = MagicMock()
        task.workflow_id = "wf-1"
        task.task_id = 42
        task.result.return_value = {"status": "Completed", "duration": 1.5}

        self.server.update_task(task=task)

        mock_patch.assert_called_once_with(
            "https://example.com/api/v1/workflows/wf-1/tasks/42",
            json={"status": "Completed", "duration": 1.5},
            headers=self.server._headers,
            timeout=15.0,
        )

    @patch("dotflow.providers.server_api.post")
    def test_network_failure_is_swallowed(self, mock_post):
        mock_post.side_effect = RequestException("connection refused")
        self.server.create_workflow(workflow="wf-1")

    @patch("dotflow.providers.server_api.patch")
    def test_update_task_network_failure_is_swallowed(self, mock_patch):
        mock_patch.side_effect = RequestException("timeout")
        task = MagicMock()
        task.workflow_id = "wf-1"
        task.task_id = 42
        task.result.return_value = {"status": "Completed"}
        self.server.update_task(task=task)

    @patch("dotflow.providers.server_api.get")
    def test_get_next_task_id_returns_value_from_api(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"last_id": 3, "next_id": 4}),
        )
        result = self.server.get_next_task_id(workflow="wf-1")
        mock_get.assert_called_once_with(
            "https://example.com/api/v1/workflows/wf-1/tasks/next-id",
            headers=self.server._headers,
            timeout=15.0,
        )
        self.assertEqual(result, 4)

    @patch("dotflow.providers.server_api.get")
    def test_get_next_task_id_defaults_to_one_on_error(self, mock_get):
        mock_get.side_effect = RequestException("boom")
        self.assertEqual(self.server.get_next_task_id(workflow="wf-1"), 1)

    @patch("dotflow.providers.server_api.get")
    def test_get_next_task_id_defaults_to_one_on_non_200(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=404,
            json=MagicMock(return_value={}),
        )
        self.assertEqual(self.server.get_next_task_id(workflow="wf-1"), 1)
