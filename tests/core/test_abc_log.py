"""Test Log ABC"""

import json
import logging
import unittest
from unittest.mock import MagicMock

from dotflow.abc.log import LEVELS, Log, LogRecord, LogRecordError
from dotflow.core.types.status import TypeStatus


class ConcreteLog(Log):

    def __init__(self, level="INFO", format="simple"):
        self._level = LEVELS.get(level.upper(), logging.INFO)
        self._format = format
        self._logger = MagicMock()


class TestLevels(unittest.TestCase):

    def test_levels_mapping(self):
        self.assertEqual(LEVELS["DEBUG"], logging.DEBUG)
        self.assertEqual(LEVELS["INFO"], logging.INFO)
        self.assertEqual(LEVELS["WARNING"], logging.WARNING)
        self.assertEqual(LEVELS["ERROR"], logging.ERROR)


class TestLogRecordError(unittest.TestCase):

    def test_defaults(self):
        error = LogRecordError()

        self.assertEqual(error.exception, "")
        self.assertEqual(error.message, "")

    def test_with_values(self):
        error = LogRecordError(exception="ValueError", message="broken")

        self.assertEqual(error.exception, "ValueError")
        self.assertEqual(error.message, "broken")


class TestLogRecord(unittest.TestCase):

    def test_defaults(self):
        record = LogRecord()

        self.assertEqual(record.timestamp, "")
        self.assertEqual(record.level, "")
        self.assertIsNone(record.duration)
        self.assertIsNone(record.retry_count)
        self.assertIsNone(record.error)

    def test_with_values(self):
        record = LogRecord(
            timestamp="2026-01-01T00:00:00",
            level="INFO",
            workflow_id="wf-1",
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            status="Completed",
            duration=1.5,
            retry_count=2,
        )

        self.assertEqual(record.workflow_id, "wf-1")
        self.assertEqual(record.duration, 1.5)
        self.assertEqual(record.retry_count, 2)

    def test_model_dump_json_excludes_none(self):
        record = LogRecord(workflow_id="wf-1", task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV")
        result = json.loads(record.model_dump_json(exclude_none=True))

        self.assertNotIn("duration", result)
        self.assertNotIn("retry_count", result)
        self.assertNotIn("error", result)

    def test_model_dump_json_includes_set_values(self):
        record = LogRecord(workflow_id="wf-1", duration=0.0)
        result = json.loads(record.model_dump_json(exclude_none=True))

        self.assertEqual(result["duration"], 0.0)


class TestLogDispatch(unittest.TestCase):

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def test_info_dispatches_to_log(self):
        log = ConcreteLog()
        task = self._make_task()

        log.info(task=task)

        log._logger.log.assert_called_once_with(
            logging.INFO, unittest.mock.ANY
        )

    def test_error_dispatches_to_log(self):
        log = ConcreteLog()
        task = self._make_task(status=TypeStatus.FAILED)

        log.error(task=task)

        log._logger.log.assert_called_once_with(
            logging.ERROR, unittest.mock.ANY
        )

    def test_warning_dispatches_to_log(self):
        log = ConcreteLog()
        task = self._make_task(status=TypeStatus.RETRY)

        log.warning(task=task)

        log._logger.log.assert_called_once_with(
            logging.WARNING, unittest.mock.ANY
        )

    def test_debug_dispatches_to_log(self):
        log = ConcreteLog(level="DEBUG")
        task = self._make_task()

        log.debug(task=task)

        log._logger.log.assert_called_once_with(
            logging.DEBUG, unittest.mock.ANY
        )

    def test_level_filter_skips_below(self):
        log = ConcreteLog(level="ERROR")

        log.info(task=self._make_task())

        log._logger.log.assert_not_called()

    def test_level_filter_allows_equal(self):
        log = ConcreteLog(level="WARNING")

        log.warning(task=self._make_task())

        log._logger.log.assert_called_once()

    def test_kwargs_without_task(self):
        log = ConcreteLog()

        log.info(workflow_id="wf-1", duration=2.5)

        log._logger.log.assert_called_once_with(
            logging.INFO, unittest.mock.ANY
        )


class TestFormatText(unittest.TestCase):

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def test_simple_task_message(self):
        log = ConcreteLog(format="simple")
        task = self._make_task()

        result = log._format_text(logging.INFO, task=task)

        self.assertIn("wf-123", result)
        self.assertIn("0", result)
        self.assertIn("Completed", result)

    def test_simple_error_includes_traceback(self):
        log = ConcreteLog(format="simple")
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.traceback = "Traceback: ValueError"
        task.errors = [error]

        result = log._format_text(logging.ERROR, task=task)

        self.assertIn("Traceback: ValueError", result)

    def test_simple_kwargs(self):
        log = ConcreteLog(format="simple")

        result = log._format_text(logging.INFO, workflow_id="wf-1")

        self.assertIn("wf-1", result)


class TestFormatJson(unittest.TestCase):

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def test_json_task_message(self):
        log = ConcreteLog(format="json")
        task = self._make_task()

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertEqual(result["workflow_id"], "wf-123")
        self.assertEqual(result["task_id"], "01ARZ3NDEKTSV4RRFFQ69G5FAV")
        self.assertEqual(result["status"], "Completed")
        self.assertEqual(result["level"], "INFO")
        self.assertIn("timestamp", result)

    def test_json_includes_duration(self):
        log = ConcreteLog(format="json")
        task = self._make_task()
        task.duration = 1.23

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertEqual(result["duration"], 1.23)

    def test_json_includes_zero_duration(self):
        log = ConcreteLog(format="json")
        task = self._make_task()
        task.duration = 0.0

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertEqual(result["duration"], 0.0)

    def test_json_excludes_none_duration(self):
        log = ConcreteLog(format="json")
        task = self._make_task()
        task.duration = None

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertNotIn("duration", result)

    def test_json_includes_retry_count(self):
        log = ConcreteLog(format="json")
        task = self._make_task()
        task.retry_count = 3

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertEqual(result["retry_count"], 3)

    def test_json_error_includes_error_details(self):
        log = ConcreteLog(format="json")
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "broken"
        task.errors = [error]

        result = json.loads(log._format_json(logging.ERROR, task=task))

        self.assertEqual(result["error"]["exception"], "ValueError")
        self.assertEqual(result["error"]["message"], "broken")

    def test_json_error_not_included_below_error_level(self):
        log = ConcreteLog(format="json")
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "broken"
        task.errors = [error]

        result = json.loads(log._format_json(logging.INFO, task=task))

        self.assertNotIn("error", result)

    def test_json_kwargs_without_task(self):
        log = ConcreteLog(format="json")

        result = json.loads(log._format_json(logging.INFO, workflow_id="wf-1"))

        self.assertEqual(result["workflow_id"], "wf-1")
