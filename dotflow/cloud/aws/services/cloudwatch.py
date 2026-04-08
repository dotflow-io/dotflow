"""CloudWatch Logs operations."""

from __future__ import annotations

import contextlib

from dotflow.cloud.core import LogManager


class CloudWatch(LogManager):
    """AWS CloudWatch log manager."""

    def __init__(self, logs_client):
        self._logs = logs_client

    def ensure_log_group(self, name: str):
        """Create log group if it doesn't exist."""
        with contextlib.suppress(
            self._logs.exceptions.ResourceAlreadyExistsException
        ):
            self._logs.create_log_group(logGroupName=name)
            print(f"  Created log group '{name}'")
