"""Test LogOpenTelemetry"""

import logging
import sys
import unittest
from unittest.mock import MagicMock

from dotflow.abc.log import Log
from dotflow.core.types.status import TypeStatus

sys.modules["opentelemetry"] = MagicMock()
sys.modules["opentelemetry._logs"] = MagicMock()
sys.modules["opentelemetry.sdk"] = MagicMock()
sys.modules["opentelemetry.sdk._logs"] = MagicMock()
sys.modules["opentelemetry.sdk._logs.export"] = MagicMock()
sys.modules["opentelemetry.sdk.resources"] = MagicMock()

from dotflow.providers.log_opentelemetry import LogOpenTelemetry  # noqa: E402


class TestLogOpenTelemetry(unittest.TestCase):
    def _make_log(self):
        log = LogOpenTelemetry(service_name="test")
        log._logger = MagicMock()
        return log

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = 0
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def test_instance(self):
        log = LogOpenTelemetry(service_name="test")

        self.assertIsInstance(log, Log)

    def test_info_with_task(self):
        log = self._make_log()
        task = self._make_task()

        log.info(task=task)

        log._logger.log.assert_called_once_with(logging.INFO, unittest.mock.ANY)

    def test_error_with_task(self):
        log = self._make_log()
        task = self._make_task(status=TypeStatus.FAILED)

        log.error(task=task)

        log._logger.log.assert_called_once_with(logging.ERROR, unittest.mock.ANY)

    def test_warning_with_task(self):
        log = self._make_log()
        task = self._make_task(status=TypeStatus.RETRY)

        log.warning(task=task)

        log._logger.log.assert_called_once_with(logging.WARNING, unittest.mock.ANY)

    def test_debug_with_task(self):
        log = self._make_log()
        log._level = logging.DEBUG
        task = self._make_task()

        log.debug(task=task)

        log._logger.log.assert_called_once_with(logging.DEBUG, unittest.mock.ANY)

    def test_info_with_kwargs(self):
        log = self._make_log()

        log.info(workflow_id="wf-1", duration=2.5)

        log._logger.log.assert_called_once_with(logging.INFO, unittest.mock.ANY)

    def test_error_with_kwargs(self):
        log = self._make_log()

        log.error(workflow_id="wf-1", message="failed")

        log._logger.log.assert_called_once_with(logging.ERROR, unittest.mock.ANY)

    def test_info_no_args(self):
        log = self._make_log()

        log.info()

        log._logger.log.assert_called_once_with(logging.INFO, unittest.mock.ANY)

    def test_debug_no_args(self):
        log = self._make_log()
        log._level = logging.DEBUG

        log.debug()

        log._logger.log.assert_called_once_with(logging.DEBUG, unittest.mock.ANY)
