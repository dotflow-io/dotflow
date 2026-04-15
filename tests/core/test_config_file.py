"""Tests for the CLI config file helpers and env>file precedence."""

from pathlib import Path
from unittest.mock import patch

import pytest

from dotflow.core.config_file import (
    clear_cloud_config,
    config_path,
    load_cloud_config,
    resolve,
    save_cloud_config,
)


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    yield tmp_path


class TestSaveAndLoad:
    def test_roundtrip(self, tmp_home):
        save_cloud_config(
            token="dtf_sk_abc", base_url="https://api.example.com"
        )
        data = load_cloud_config()
        assert data == {
            "base_url": "https://api.example.com",
            "token": "dtf_sk_abc",
        }

    def test_file_is_written_with_0600_perms(self, tmp_home):
        save_cloud_config(token="t", base_url="b")
        mode = config_path().stat().st_mode & 0o777
        assert mode == 0o600

    def test_load_returns_empty_when_missing(self, tmp_home):
        assert load_cloud_config() == {}

    def test_handles_special_chars_in_values(self, tmp_home):
        save_cloud_config(token='tok"en\\x', base_url="url with space")
        data = load_cloud_config()
        assert data["token"] == 'tok"en\\x'
        assert data["base_url"] == "url with space"

    def test_ignores_other_sections(self, tmp_home):
        import json

        config_path().parent.mkdir(parents=True, exist_ok=True)
        config_path().write_text(
            json.dumps(
                {
                    "cloud": {
                        "token": "abc",
                        "base_url": "http://x",
                    },
                    "other": {"token": "ignored"},
                }
            )
        )
        assert load_cloud_config() == {
            "token": "abc",
            "base_url": "http://x",
        }

    def test_returns_empty_on_invalid_json(self, tmp_home):
        config_path().parent.mkdir(parents=True, exist_ok=True)
        config_path().write_text("not { valid json")
        assert load_cloud_config() == {}


class TestClear:
    def test_removes_file(self, tmp_home):
        save_cloud_config(token="t", base_url="b")
        assert clear_cloud_config() is True
        assert not config_path().exists()

    def test_returns_false_when_file_missing(self, tmp_home):
        assert clear_cloud_config() is False


class TestResolvePrecedence:
    def test_env_wins_over_file(self, tmp_home):
        save_cloud_config(token="file-token", base_url="file-url")
        with patch.dict(
            "os.environ",
            {"SERVER_USER_TOKEN": "env-token"},
            clear=False,
        ):
            assert resolve("token", "SERVER_USER_TOKEN") == "env-token"

    def test_file_used_when_env_missing(self, tmp_home, monkeypatch):
        monkeypatch.delenv("SERVER_USER_TOKEN", raising=False)
        save_cloud_config(token="file-token", base_url="file-url")
        assert resolve("token", "SERVER_USER_TOKEN") == "file-token"

    def test_returns_none_when_nothing_set(self, tmp_home, monkeypatch):
        monkeypatch.delenv("SERVER_USER_TOKEN", raising=False)
        assert resolve("token", "SERVER_USER_TOKEN") is None

    def test_empty_env_falls_back_to_file(self, tmp_home, monkeypatch):
        monkeypatch.setenv("SERVER_USER_TOKEN", "")
        save_cloud_config(token="file-token", base_url="b")
        assert resolve("token", "SERVER_USER_TOKEN") == "file-token"
