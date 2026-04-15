"""Command login module."""

from __future__ import annotations

import os
import time
import webbrowser

from requests import RequestException, post
from rich import print  # type: ignore

from dotflow.cli.command import Command
from dotflow.core.config_file import save_cloud_config
from dotflow.settings import Settings as settings

DEFAULT_BASE_URLS = (
    "https://www.cli.dotflow.io/api/v1",
)
DEFAULT_BASE_URL = DEFAULT_BASE_URLS[0]
DEVICE_ENDPOINT = "/auth/cli/device"
TOKEN_ENDPOINT = "/auth/cli/token"
TIMEOUT = 15
DEFAULT_INTERVAL = 5


class LoginCommand(Command):

    def setup(self):
        token = getattr(self.params, "token", None)

        if token:
            base_url = self._explicit_base_url() or DEFAULT_BASE_URL
            save_cloud_config(token=token, base_url=base_url)
            print(settings.INFO_ALERT, "Token saved.")
            return

        handshake_result = self._start_device_with_fallback()

        if handshake_result is None:
            return

        base_url, handshake = handshake_result

        print(settings.INFO_ALERT, f"Opening {handshake['verification_uri']}")
        print(settings.INFO_ALERT, f"Code: {handshake['user_code']}")

        webbrowser.open(handshake["verification_uri"])

        token = self._poll_token(base_url, handshake)

        if not token:
            return

        save_cloud_config(token=token, base_url=base_url)
        print(settings.INFO_ALERT, "Authenticated.")

    def _explicit_base_url(self) -> str | None:
        """Return the user-provided base URL (flag/env), or ``None``."""
        explicit = getattr(self.params, "base_url", None) or os.environ.get(
            "SERVER_BASE_URL"
        )
        return explicit.rstrip("/") if explicit else None

    def _candidate_base_urls(self) -> list[str]:
        """URLs to try in order. Explicit flag/env always wins and skips fallback."""
        explicit = self._explicit_base_url()

        if explicit:
            return [explicit]
        return list(DEFAULT_BASE_URLS)

    def _start_device_with_fallback(self) -> tuple[str, dict] | None:
        """Try each candidate base URL until one responds; returns (url, payload)."""
        last_error: Exception | None = None

        for base_url in self._candidate_base_urls():
            try:
                payload = self._start_device(base_url)
                return base_url, payload
            except RequestException as error:
                last_error = error
                continue

        print(
            settings.ERROR_ALERT,
            f"Could not reach Dotflow Cloud: {last_error}",
        )
        return None

    def _start_device(self, base_url: str) -> dict:
        response = post(f"{base_url}{DEVICE_ENDPOINT}", timeout=TIMEOUT)
        response.raise_for_status()

        return response.json()

    def _poll_token(self, base_url: str, handshake: dict) -> str | None:
        interval = handshake.get("interval") or DEFAULT_INTERVAL
        deadline = time.monotonic() + (handshake.get("expires_in") or 300)

        while time.monotonic() < deadline:
            try:
                response = post(
                    f"{base_url}{TOKEN_ENDPOINT}",
                    json={"device_code": handshake["device_code"]},
                    timeout=TIMEOUT,
                )
            except RequestException as error:
                print(settings.ERROR_ALERT, f"Network error: {error}")
                return None

            if response.status_code == 200:
                return response.json().get("api_token")

            detail = self._detail(response)

            if (
                response.status_code == 400
                and detail == "authorization_pending"
            ):
                time.sleep(interval)
                continue

            if (
                response.status_code == 400
                and detail in ("slow_down", "slow down")
            ):
                interval += 5
                time.sleep(interval)
                continue

            if response.status_code == 410:
                print(settings.ERROR_ALERT, "Authorization expired.")
                return None

            print(settings.ERROR_ALERT, f"{response.status_code}: {detail}")
            return None

        print(settings.ERROR_ALERT, "Timed out waiting for authorization.")
        return None

    @staticmethod
    def _detail(response) -> str:
        try:
            return str(response.json().get("detail", response.text))
        except ValueError:
            return response.text
