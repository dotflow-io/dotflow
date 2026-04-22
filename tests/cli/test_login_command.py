"""Tests for LoginCommand and LogoutCommand."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dotflow.cli.commands.login import LoginCommand
from dotflow.cli.commands.logout import LogoutCommand


def _make_cmd(cls):
    cmd = cls.__new__(cls)
    cmd.params = SimpleNamespace()
    return cmd


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.delenv("SERVER_BASE_URL", raising=False)
    yield tmp_path


class TestLoginDeviceFlow:
    def test_persists_token_on_successful_poll(self, tmp_home):
        handshake = MagicMock()
        handshake.status_code = 201
        handshake.json.return_value = {
            "device_code": "device-xyz",
            "user_code": "ABCD-1234",
            "verification_uri": "https://cloud.dotflow.io/cli?code=ABCD-1234",
            "interval": 0,
            "expires_in": 60,
        }
        handshake.raise_for_status = MagicMock()

        pending = MagicMock()
        pending.status_code = 400
        pending.json.return_value = {"detail": "authorization_pending"}

        ok = MagicMock()
        ok.status_code = 200
        ok.json.return_value = {"api_token": "dtf_sk_from_browser"}

        cmd = _make_cmd(LoginCommand)
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=[handshake, pending, ok],
            ) as mock_post,
            patch(
                "dotflow.cli.commands.login.webbrowser.open"
            ) as mock_browser,
        ):
            cmd.setup()

        assert mock_post.call_count == 3
        mock_browser.assert_called_once_with(
            "https://cloud.dotflow.io/cli?code=ABCD-1234"
        )
        config = tmp_home / ".dotflow" / "config.json"
        assert '"token": "dtf_sk_from_browser"' in config.read_text()

    def test_aborts_when_authorization_gone(self, tmp_home):
        handshake = MagicMock()
        handshake.status_code = 201
        handshake.json.return_value = {
            "device_code": "d",
            "user_code": "A-B",
            "verification_uri": "https://x",
            "interval": 0,
            "expires_in": 60,
        }
        handshake.raise_for_status = MagicMock()

        gone = MagicMock()
        gone.status_code = 410
        gone.json.return_value = {"detail": "Device code expired"}

        cmd = _make_cmd(LoginCommand)
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=[handshake, gone],
            ),
            patch("dotflow.cli.commands.login.webbrowser.open"),
        ):
            cmd.setup()

        assert not (tmp_home / ".dotflow" / "config.json").exists()

    def test_env_var_overrides_default_base_url(self, tmp_home, monkeypatch):
        from requests import ConnectionError as RequestsConnectionError

        monkeypatch.setenv("SERVER_BASE_URL", "https://only.local")

        cmd = _make_cmd(LoginCommand)
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=RequestsConnectionError("unreachable"),
            ) as mock_post,
            patch("dotflow.cli.commands.login.webbrowser.open"),
        ):
            cmd.setup()

        assert mock_post.call_count == 1
        assert mock_post.call_args.args[0].startswith("https://only.local")
        assert not (tmp_home / ".dotflow" / "config.json").exists()


class TestLogout:
    def test_deletes_config_file(self, tmp_home):
        (tmp_home / ".dotflow").mkdir(parents=True, exist_ok=True)
        (tmp_home / ".dotflow" / "config.json").write_text(
            '{"cloud": {"token": "x"}}'
        )

        cmd = _make_cmd(LogoutCommand)
        cmd.setup()

        assert not (tmp_home / ".dotflow" / "config.json").exists()

    def test_is_noop_when_no_config(self, tmp_home):
        cmd = _make_cmd(LogoutCommand)
        cmd.setup()
        assert not (tmp_home / ".dotflow" / "config.json").exists()
