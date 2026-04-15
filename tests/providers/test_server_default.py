import unittest
from unittest.mock import patch

from dotflow.providers.server_default import ServerDefault


class TestServerDefault(unittest.TestCase):
    def setUp(self):
        self._cfg_patch = patch(
            "dotflow.core.config_file.load_cloud_config",
            return_value={},
        )
        self._cfg_patch.start()

    def tearDown(self):
        self._cfg_patch.stop()

    @patch.dict("os.environ", {}, clear=True)
    def test_instantiation(self):
        server = ServerDefault()
        self.assertIsInstance(server, ServerDefault)

    @patch.dict("os.environ", {}, clear=True)
    def test_not_managed_without_env_vars(self):
        server = ServerDefault()
        self.assertFalse(server._managed)

    @patch.dict(
        "os.environ",
        {
            "SERVER_BASE_URL": "https://x.example/api/v1",
            "SERVER_USER_TOKEN": "tok-abc",
        },
    )
    def test_managed_when_both_env_vars_set(self):
        server = ServerDefault()
        self.assertTrue(server._managed)

    @patch.dict("os.environ", {"SERVER_BASE_URL": "https://x.example/api/v1"})
    def test_not_managed_when_only_base_url_set(self):
        server = ServerDefault()
        self.assertFalse(server._managed)

    @patch.dict("os.environ", {"SERVER_USER_TOKEN": "tok"})
    def test_not_managed_when_only_token_set(self):
        server = ServerDefault()
        self.assertFalse(server._managed)

    @patch.dict("os.environ", {}, clear=True)
    def test_create_workflow_noop(self):
        server = ServerDefault()
        server.create_workflow(workflow="wf-1")

    @patch.dict("os.environ", {}, clear=True)
    def test_update_workflow_noop(self):
        server = ServerDefault()
        server.update_workflow(workflow="wf-1", status="Completed")

    @patch.dict("os.environ", {}, clear=True)
    def test_create_task_noop(self):
        server = ServerDefault()
        server.create_task(task=None)

    @patch.dict("os.environ", {}, clear=True)
    def test_update_task_noop(self):
        server = ServerDefault()
        server.update_task(task=None)
