"""Tests for StartCommand."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dotflow.cli.commands.start import StartCommand
from dotflow.core.exception import InvalidWorkflowFactory, WorkflowFlagConflict
from dotflow.providers import ServerAPI, ServerDefault
from dotflow.utils.basic_functions import basic_callback


def _make_cmd(**kwargs):
    defaults = {
        "step": None,
        "workflow": None,
        "callback": basic_callback,
        "initial_context": None,
        "storage": None,
        "path": "/tmp",
        "mode": "sequential",
    }
    defaults.update(kwargs)
    cmd = StartCommand.__new__(StartCommand)
    cmd.params = SimpleNamespace(**defaults)
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


class TestStartFromFactory:
    def test_raises_when_factory_not_callable(self):
        cmd = _make_cmd(
            workflow="dotflow.core.exception.MESSAGE_UNKNOWN_ERROR"
        )
        with pytest.raises(InvalidWorkflowFactory):
            cmd._start_from_factory()

    def test_raises_when_factory_returns_non_dotflow(self):
        cmd = _make_cmd(
            workflow="dotflow.utils.basic_functions.basic_callback"
        )
        with pytest.raises(InvalidWorkflowFactory):
            cmd._start_from_factory()

    def test_raises_on_callback_flag_conflict(self):
        custom_cb = MagicMock()
        cmd = _make_cmd(
            workflow="dotflow.utils.basic_functions.basic_callback",
            callback=custom_cb,
        )
        with pytest.raises(WorkflowFlagConflict):
            cmd._start_from_factory()

    def test_raises_on_initial_context_flag_conflict(self):
        cmd = _make_cmd(
            workflow="dotflow.utils.basic_functions.basic_callback",
            initial_context="abc",
        )
        with pytest.raises(WorkflowFlagConflict):
            cmd._start_from_factory()

    def test_valid_factory_calls_start(self):
        mock_workflow = MagicMock()

        def factory():
            return mock_workflow

        with (
            patch("dotflow.cli.commands.start.Module", return_value=factory),
            patch("dotflow.cli.commands.start.isinstance", return_value=True),
        ):
            cmd = _make_cmd(workflow="mymod.factory")
            cmd._start_from_factory()

        mock_workflow.start.assert_called_once_with(mode="sequential")
