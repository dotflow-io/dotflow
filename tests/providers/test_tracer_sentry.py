"""Test TracerSentry"""

import sys
import unittest
from unittest.mock import MagicMock

from dotflow.abc.tracer import Tracer
from dotflow.core.types.status import TypeStatus

mock_sentry_sdk = MagicMock()
sys.modules["sentry_sdk"] = mock_sentry_sdk

from dotflow.providers.tracer_sentry import TracerSentry  # noqa: E402, I001


class TestTracerSentry(unittest.TestCase):

    def _make_tracer(self):
        tracer = TracerSentry()
        tracer._sentry = MagicMock()
        return tracer

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
        task.duration = 0.5
        task.retry_count = 0
        task.errors = []
        return task

    def test_instance(self):
        tracer = TracerSentry()

        self.assertIsInstance(tracer, Tracer)

    def test_init_with_dsn_calls_sentry_init(self):
        sentry_mock = sys.modules["sentry_sdk"]
        sentry_mock.reset_mock()

        TracerSentry(
            dsn="https://test@sentry.io/1",
            environment="staging",
            traces_sample_rate=0.8,
        )

        sentry_mock.init.assert_called_once_with(
            dsn="https://test@sentry.io/1",
            environment="staging",
            traces_sample_rate=0.8,
        )

    def test_init_without_dsn_skips_init(self):
        sentry_mock = sys.modules["sentry_sdk"]
        sentry_mock.reset_mock()

        TracerSentry()

        sentry_mock.init.assert_not_called()

    def test_start_workflow_creates_transaction(self):
        tracer = self._make_tracer()

        tracer.start_workflow(workflow_id="wf-1", mode="sequential")

        tracer._sentry.start_transaction.assert_called_once_with(
            op="workflow",
            name="workflow:wf-1",
        )
        self.assertIn("wf-1", tracer._transactions)

    def test_end_workflow_finishes_transaction(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-1")
        transaction = tracer._transactions["wf-1"]

        tracer.end_workflow(workflow_id="wf-1", duration=2.5, failed=False)

        transaction.set_status.assert_called_with("ok")
        transaction.finish.assert_called_once()
        self.assertNotIn("wf-1", tracer._transactions)

    def test_end_workflow_failed_sets_error_status(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-1")
        transaction = tracer._transactions["wf-1"]

        tracer.end_workflow(workflow_id="wf-1", failed=True)

        transaction.set_status.assert_called_with("internal_error")

    def test_end_workflow_not_started(self):
        tracer = self._make_tracer()

        tracer.end_workflow(workflow_id="nonexistent")

    def test_start_task_creates_child_span(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-123")
        task = self._make_task()

        tracer.start_task(task=task)

        transaction = tracer._transactions["wf-123"]
        transaction.start_child.assert_called_once_with(
            op="task",
            name="task:01ARZ3NDEKTSV4RRFFQ69G5FAV",
        )
        self.assertIn("wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV", tracer._spans)

    def test_start_task_without_transaction(self):
        tracer = self._make_tracer()
        task = self._make_task()

        tracer.start_task(task=task)

        self.assertNotIn("wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV", tracer._spans)

    def test_end_task_finishes_span(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-123")
        task = self._make_task()
        tracer.start_task(task=task)
        span = tracer._spans["wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV"]

        tracer.end_task(task=task)

        span.set_status.assert_called_with("ok")
        span.finish.assert_called_once()
        self.assertNotIn("wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV", tracer._spans)

    def test_end_task_with_errors_sets_error_status(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-123")
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        task.errors = [error]
        tracer.start_task(task=task)
        span = tracer._spans["wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV"]

        tracer.end_task(task=task)

        span.set_status.assert_called_with("internal_error")
        span.set_data.assert_any_call("dotflow.task.exception", "ValueError")

    def test_end_task_records_duration(self):
        tracer = self._make_tracer()
        tracer.start_workflow(workflow_id="wf-123")
        task = self._make_task()
        task.duration = 1.23
        tracer.start_task(task=task)
        span = tracer._spans["wf-123:01ARZ3NDEKTSV4RRFFQ69G5FAV"]

        tracer.end_task(task=task)

        span.set_data.assert_any_call("dotflow.task.duration", 1.23)

    def test_end_task_not_started(self):
        tracer = self._make_tracer()
        task = self._make_task()

        tracer.end_task(task=task)
