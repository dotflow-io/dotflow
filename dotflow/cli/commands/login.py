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

DEFAULT_BASE_URL = "https://www.cli.dotflow.io/api/v1"
DEVICE_ENDPOINT = "/auth/cli/device"
TOKEN_ENDPOINT = "/auth/cli/token"
TIMEOUT = 15
DEFAULT_INTERVAL = 5


class LoginCommand(Command):

    def setup(self):
        token = getattr(self.params, "token", None)
        base_url = self._resolve_base_url()

        if token:
            save_cloud_config(token=token, base_url=base_url)
            print(settings.INFO_ALERT, "Token saved.")
            return

        handshake = self._start_device(base_url)
        if handshake is None:
            return

        print(settings.INFO_ALERT, f"Opening {handshake['verification_uri']}")
        print(settings.INFO_ALERT, f"Code: {handshake['user_code']}")

        webbrowser.open(handshake["verification_uri"])

        token = self._poll_token(base_url, handshake)

        if not token:
            return

        save_cloud_config(token=token, base_url=base_url)
        print(settings.INFO_ALERT, "Authenticated.")

    def _resolve_base_url(self) -> str:
        """Flag or env var wins over the default."""
        explicit = getattr(self.params, "base_url", None) or os.environ.get(
            "SERVER_BASE_URL"
        )
        return explicit.rstrip("/") if explicit else DEFAULT_BASE_URL

    def _start_device(self, base_url: str) -> dict | None:
        try:
            response = post(
                f"{base_url}{DEVICE_ENDPOINT}",
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except RequestException as error:
            print(
                settings.ERROR_ALERT,
                f"Could not reach Dotflow Cloud: {error}",
            )
            return None

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
