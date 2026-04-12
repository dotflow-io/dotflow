"""Tests for dotflow.cli.commands.start.StartCommand managed-mode wiring."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from dotflow.cli.commands.start import StartCommand
from dotflow.providers import ServerAPI, ServerDefault


def _make_cmd(**kwargs):
    """Build a StartCommand without running setup()."""
    cmd = StartCommand.__new__(StartCommand)
    cmd.params = SimpleNamespace(
        step="mod:attr",
        callback=None,
        initial_context=None,
        storage=None,
        path="/tmp",
        mode="sequential",
        **kwargs,
    )
    return cmd


class TestBuildServer(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    def test_returns_none_when_both_env_vars_missing(self):
        cmd = _make_cmd()
        self.assertIsNone(cmd._build_server())

    @patch.dict("os.environ", {"SERVER_BASE_URL": "https://x.example/api/v1"})
    def test_returns_none_when_only_base_url_set(self):
        cmd = _make_cmd()
        self.assertIsNone(cmd._build_server())

    @patch.dict("os.environ", {"SERVER_USER_TOKEN": "tok"})
    def test_returns_none_when_only_token_set(self):
        cmd = _make_cmd()
        self.assertIsNone(cmd._build_server())

    @patch.dict(
        "os.environ",
        {
            "SERVER_BASE_URL": "https://x.example/api/v1",
            "SERVER_USER_TOKEN": "tok-abc",
        },
    )
    def test_returns_server_api_when_both_set(self):
        cmd = _make_cmd()
        server = cmd._build_server()
        self.assertIsInstance(server, ServerAPI)
        self.assertEqual(server._base_url, "https://x.example/api/v1")
        self.assertEqual(server._user_token, "tok-abc")


class TestBuildConfig(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    def test_returns_none_when_no_storage_and_no_server(self):
        cmd = _make_cmd()
        self.assertIsNone(cmd._build_config())

    @patch.dict(
        "os.environ",
        {
            "SERVER_BASE_URL": "https://x.example/api/v1",
            "SERVER_USER_TOKEN": "tok-abc",
        },
    )
    def test_builds_config_with_server_when_env_present(self):
        cmd = _make_cmd()
        config = cmd._build_config()
        self.assertIsNotNone(config)
        self.assertIsInstance(config.server, ServerAPI)


class TestNewWorkflow(unittest.TestCase):
    @patch("dotflow.cli.commands.start.DotFlow")
    @patch.dict("os.environ", {}, clear=True)
    def test_passes_none_workflow_id_when_env_missing(self, mock_dotflow):
        cmd = _make_cmd()
        cmd._new_workflow()
        mock_dotflow.assert_called_once_with(workflow_id=None)

    @patch("dotflow.cli.commands.start.DotFlow")
    @patch.dict(
        "os.environ",
        {"WORKFLOW_ID": "external-uuid"},
        clear=True,
    )
    def test_passes_workflow_id_from_env(self, mock_dotflow):
        cmd = _make_cmd()
        cmd._new_workflow()
        mock_dotflow.assert_called_once_with(workflow_id="external-uuid")

    @patch("dotflow.cli.commands.start.DotFlow")
    @patch.dict(
        "os.environ",
        {
            "SERVER_BASE_URL": "https://x.example/api/v1",
            "SERVER_USER_TOKEN": "tok-abc",
            "WORKFLOW_ID": "external-uuid",
        },
        clear=True,
    )
    def test_passes_config_and_workflow_id_in_managed_mode(self, mock_dotflow):
        cmd = _make_cmd()
        cmd._new_workflow()
        mock_dotflow.assert_called_once()
        args, kwargs = mock_dotflow.call_args
        self.assertEqual(kwargs["workflow_id"], "external-uuid")
        self.assertIsInstance(kwargs["config"].server, ServerAPI)

    @patch("dotflow.cli.commands.start.DotFlow")
    @patch.dict("os.environ", {}, clear=True)
    def test_stand_alone_mode_uses_default_server(self, mock_dotflow):
        cmd = _make_cmd()
        cmd._new_workflow()
        _, kwargs = mock_dotflow.call_args
        self.assertNotIn("config", kwargs)
        self.assertIsNone(kwargs["workflow_id"])

        config = MagicMock()
        config.server = ServerDefault()
        self.assertIsInstance(config.server, ServerDefault)
