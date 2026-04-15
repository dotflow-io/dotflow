"""Tests for LoginCommand and LogoutCommand."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dotflow.cli.commands.login import LoginCommand
from dotflow.cli.commands.logout import LogoutCommand


def _params(**kwargs) -> SimpleNamespace:
    defaults = {"base_url": None, "token": None}
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _make_cmd(cls, params: SimpleNamespace):
    cmd = cls.__new__(cls)
    cmd.params = params
    return cmd


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    yield tmp_path


class TestLoginWithExplicitToken:
    def test_saves_token_without_network_calls(self, tmp_home):
        cmd = _make_cmd(
            LoginCommand,
            _params(token="dtf_sk_direct", base_url="https://api.local"),
        )
        with (
            patch("dotflow.cli.commands.login.post") as mock_post,
            patch(
                "dotflow.cli.commands.login.webbrowser.open"
            ) as mock_browser,
        ):
            cmd.setup()
            mock_post.assert_not_called()
            mock_browser.assert_not_called()

        config = tmp_home / ".dotflow" / "config.toml"
        assert config.exists()
        content = config.read_text()
        assert 'token = "dtf_sk_direct"' in content
        assert 'base_url = "https://api.local"' in content


class TestLoginDeviceFlow:
    def _responses(self, *items):
        for item in items:
            r = MagicMock()
            r.status_code = item[0]
            if len(item) > 1:
                r.json.return_value = item[1]
            else:
                r.json.return_value = {}
            yield r

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

        cmd = _make_cmd(
            LoginCommand,
            _params(base_url="https://api.local"),
        )
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
        config = tmp_home / ".dotflow" / "config.toml"
        assert 'token = "dtf_sk_from_browser"' in config.read_text()

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

        cmd = _make_cmd(LoginCommand, _params(base_url="https://api.local"))
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=[handshake, gone],
            ),
            patch("dotflow.cli.commands.login.webbrowser.open"),
        ):
            cmd.setup()

        assert not (tmp_home / ".dotflow" / "config.toml").exists()

    def test_falls_back_to_next_base_url_when_first_fails(self, tmp_home):
        from requests import ConnectionError as RequestsConnectionError

        from dotflow.cli.commands.login import DEFAULT_BASE_URLS

        handshake = MagicMock()
        handshake.status_code = 201
        handshake.json.return_value = {
            "device_code": "d",
            "user_code": "AAAA-0000",
            "verification_uri": "https://x",
            "interval": 0,
            "expires_in": 60,
        }
        handshake.raise_for_status = MagicMock()

        ok = MagicMock()
        ok.status_code = 200
        ok.json.return_value = {"api_token": "dtf_sk_second"}

        cmd = _make_cmd(LoginCommand, _params())
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=[
                    RequestsConnectionError("first down"),
                    handshake,
                    ok,
                ],
            ) as mock_post,
            patch("dotflow.cli.commands.login.webbrowser.open"),
        ):
            cmd.setup()

        assert (
            mock_post.call_args_list[0]
            .args[0]
            .startswith(DEFAULT_BASE_URLS[0])
        )
        assert (
            mock_post.call_args_list[1]
            .args[0]
            .startswith(DEFAULT_BASE_URLS[1])
        )

        config = tmp_home / ".dotflow" / "config.toml"
        assert 'token = "dtf_sk_second"' in config.read_text()
        assert f'base_url = "{DEFAULT_BASE_URLS[1]}"' in config.read_text()

    def test_explicit_base_url_skips_fallback(self, tmp_home):
        from requests import ConnectionError as RequestsConnectionError

        cmd = _make_cmd(LoginCommand, _params(base_url="https://only.local"))
        with (
            patch(
                "dotflow.cli.commands.login.post",
                side_effect=RequestsConnectionError("unreachable"),
            ) as mock_post,
            patch("dotflow.cli.commands.login.webbrowser.open"),
        ):
            cmd.setup()

        assert mock_post.call_count == 1
        assert not (tmp_home / ".dotflow" / "config.toml").exists()


class TestLogout:
    def test_deletes_config_file(self, tmp_home):
        (tmp_home / ".dotflow").mkdir(parents=True, exist_ok=True)
        (tmp_home / ".dotflow" / "config.toml").write_text(
            '[cloud]\ntoken = "x"\n'
        )

        cmd = _make_cmd(LogoutCommand, _params())
        cmd.setup()

        assert not (tmp_home / ".dotflow" / "config.toml").exists()

    def test_is_noop_when_no_config(self, tmp_home):
        cmd = _make_cmd(LogoutCommand, _params())
        cmd.setup()  # no error expected
