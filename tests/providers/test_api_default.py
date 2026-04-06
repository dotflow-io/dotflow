"""Test ApiDefault provider"""

import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from dotflow.providers.api_default import ApiDefault


class TestApiDefaultInit(unittest.TestCase):

    def test_enabled_false_when_env_not_set(self):
        api = ApiDefault()
        self.assertFalse(api.enabled)

    def test_enabled_true_when_env_set(self):
        with patch.dict("os.environ", {"DOTFLOW_API_ENABLED": "1"}):
            api = ApiDefault()
        self.assertTrue(api.enabled)

    def test_enabled_override_true(self):
        api = ApiDefault(enabled=True)
        self.assertTrue(api.enabled)

    def test_enabled_override_false(self):
        with patch.dict("os.environ", {"DOTFLOW_API_ENABLED": "1"}):
            api = ApiDefault(enabled=False)
        self.assertFalse(api.enabled)

    def test_base_url_from_param(self):
        api = ApiDefault(base_url="http://localhost:8000/")
        self.assertEqual(api.base_url, "http://localhost:8000")

    def test_base_url_from_env(self):
        with patch.dict("os.environ", {"DOTFLOW_API_URL": "http://env-url"}):
            api = ApiDefault()
        self.assertEqual(api.base_url, "http://env-url")

    def test_user_token_from_param(self):
        api = ApiDefault(user_token="my-token")
        self.assertEqual(api.user_token, "my-token")

    def test_user_token_from_env(self):
        with patch.dict("os.environ", {"DOTFLOW_USER_TOKEN": "env-token"}):
            api = ApiDefault()
        self.assertEqual(api.user_token, "env-token")


class TestApiDefaultIsReady(unittest.TestCase):

    def test_not_ready_when_disabled(self):
        api = ApiDefault(enabled=False)
        self.assertFalse(api._is_ready())

    def test_not_ready_when_base_url_missing(self):
        api = ApiDefault(enabled=True, user_token="token")
        api.base_url = ""
        self.assertFalse(api._is_ready())

    def test_not_ready_when_user_token_missing(self):
        api = ApiDefault(enabled=True, base_url="http://localhost")
        api.user_token = None
        self.assertFalse(api._is_ready())

    def test_ready_when_all_set(self):
        api = ApiDefault(
            enabled=True,
            base_url="http://localhost",
            user_token="token",
        )
        self.assertTrue(api._is_ready())


class TestApiDefaultCallablePath(unittest.TestCase):

    def test_none_returns_none(self):
        self.assertIsNone(ApiDefault._callable_path(None))

    def test_string_returns_string(self):
        self.assertEqual(
            ApiDefault._callable_path("my.module.func"), "my.module.func"
        )

    def test_callable_returns_module_name(self):
        def my_func():
            pass

        result = ApiDefault._callable_path(my_func)
        self.assertIn("my_func", result)

    def test_object_without_module_returns_str(self):
        obj = object()
        result = ApiDefault._callable_path(obj)
        self.assertIsInstance(result, str)


class TestApiDefaultWorkflowToPayload(unittest.TestCase):

    def test_with_uuid_workflow(self):
        api = ApiDefault()
        workflow_id = uuid4()
        payload = api._workflow_to_payload(workflow_id)

        self.assertEqual(payload["id"], str(workflow_id))
        self.assertEqual(payload["tasks"], [])

    def test_with_string_workflow(self):
        api = ApiDefault()
        payload = api._workflow_to_payload("workflow-id-123")

        self.assertEqual(payload["id"], "workflow-id-123")

    def test_with_object_with_tasks(self):
        api = ApiDefault()

        task = MagicMock()
        task.task_id = 1
        task.step = None
        task.callback = None
        task.initial_context.storage = "data"
        task.group_name = "default"

        workflow = MagicMock()
        workflow.tasks = [task]

        payload = api._workflow_to_payload(workflow)

        self.assertEqual(len(payload["tasks"]), 1)
        self.assertEqual(payload["tasks"][0]["id"], 1)

    def test_execution_mode_default(self):
        api = ApiDefault()
        payload = api._workflow_to_payload("wf")

        self.assertEqual(payload["execution_mode"], "sequential")
        self.assertFalse(payload["keep_going"])


class TestApiDefaultCreateWorkflow(unittest.TestCase):

    def test_does_nothing_when_not_ready(self):
        api = ApiDefault(enabled=False)
        result = api.create_workflow("workflow")
        self.assertIsNone(result)

    def test_calls_post_when_ready(self):
        api = ApiDefault(
            enabled=True,
            base_url="http://localhost",
            user_token="token",
        )

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        with patch(
            "dotflow.providers.api_default.post", return_value=mock_response
        ):
            api.create_workflow("workflow-id")

        mock_response.raise_for_status.assert_called_once()

    def test_logs_error_on_exception(self):
        api = ApiDefault(
            enabled=True,
            base_url="http://localhost",
            user_token="token",
        )

        with patch(
            "dotflow.providers.api_default.post", side_effect=Exception("fail")
        ):
            result = api.create_workflow("workflow-id")

        self.assertIsNone(result)


class TestApiDefaultNoOps(unittest.TestCase):

    def test_update_workflow_returns_none(self):
        api = ApiDefault()
        self.assertIsNone(api.update_workflow("wf"))

    def test_create_task_returns_none(self):
        api = ApiDefault()
        self.assertIsNone(api.create_task(MagicMock()))

    def test_update_task_returns_none(self):
        api = ApiDefault()
        self.assertIsNone(api.update_task(MagicMock()))
