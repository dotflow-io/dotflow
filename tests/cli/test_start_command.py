"""Tests for StartCommand --workflow factory validation."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dotflow import DotFlow
from dotflow.cli.commands.start import StartCommand
from dotflow.core.exception import InvalidWorkflowFactory, WorkflowFlagConflict
from dotflow.utils.basic_functions import basic_callback


def _make_cmd(**kwargs):
    defaults = dict(
        step=None,
        workflow=None,
        callback=basic_callback,
        initial_context=None,
        storage=None,
        path="/tmp",
        mode="sequential",
    )
    defaults.update(kwargs)
    cmd = StartCommand.__new__(StartCommand)
    cmd.params = SimpleNamespace(**defaults)
    return cmd


class TestStartFromFactory:
    def test_raises_when_factory_not_callable(self):
        cmd = _make_cmd(workflow="dotflow.core.exception.MESSAGE_UNKNOWN_ERROR")
        with pytest.raises(InvalidWorkflowFactory):
            cmd._start_from_factory()

    def test_raises_when_factory_returns_non_dotflow(self):
        cmd = _make_cmd(workflow="dotflow.utils.basic_functions.basic_callback")
        with pytest.raises(InvalidWorkflowFactory):
            cmd._start_from_factory()

    def test_raises_on_callback_flag_conflict(self):
        custom_cb = MagicMock()
        cmd = _make_cmd(workflow="dotflow.utils.basic_functions.basic_callback", callback=custom_cb)
        with pytest.raises(WorkflowFlagConflict):
            cmd._start_from_factory()

    def test_raises_on_initial_context_flag_conflict(self):
        cmd = _make_cmd(workflow="dotflow.utils.basic_functions.basic_callback", initial_context="abc")
        with pytest.raises(WorkflowFlagConflict):
            cmd._start_from_factory()

    def test_valid_factory_calls_start(self):
        mock_workflow = MagicMock()

        def factory():
            return mock_workflow

        with patch("dotflow.cli.commands.start.Module", return_value=factory):
            with patch("dotflow.cli.commands.start.isinstance", return_value=True):
                cmd = _make_cmd(workflow="mymod.factory")
                cmd._start_from_factory()

        mock_workflow.start.assert_called_once_with(mode="sequential")
