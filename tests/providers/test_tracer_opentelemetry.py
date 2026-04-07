"""Test TracerOpenTelemetry"""

import sys
import unittest
from unittest.mock import MagicMock

from dotflow.abc.tracer import Tracer
from dotflow.core.types.status import TypeStatus

mock_otel_trace = MagicMock()
mock_otel_sdk_trace = MagicMock()
mock_otel_sdk_resources = MagicMock()
sys.modules["opentelemetry"] = MagicMock()
sys.modules["opentelemetry.trace"] = mock_otel_trace
sys.modules["opentelemetry.sdk"] = MagicMock()
sys.modules["opentelemetry.sdk.trace"] = mock_otel_sdk_trace
sys.modules["opentelemetry.sdk.resources"] = mock_otel_sdk_resources

from dotflow.providers.tracer_opentelemetry import TracerOpenTelemetry  # noqa: E402, I001


class TestTracerOpenTelemetry(unittest.TestCase):
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
        tracer = TracerOpenTelemetry(service_name="test")

        self.assertIsInstance(tracer, Tracer)

    def test_start_workflow_creates_span(self):
        tracer = TracerOpenTelemetry(service_name="test")

        tracer.start_workflow(workflow_id="wf-1", mode="sequential")

        self.assertIn("wf-1", tracer._spans)

    def test_end_workflow_removes_span(self):
        tracer = TracerOpenTelemetry(service_name="test")
        tracer.start_workflow(workflow_id="wf-1")

        tracer.end_workflow(workflow_id="wf-1")

        self.assertNotIn("wf-1", tracer._spans)

    def test_start_task_creates_span(self):
        tracer = TracerOpenTelemetry(service_name="test")
        task = self._make_task()
        tracer.start_workflow(workflow_id="wf-123")

        tracer.start_task(task=task)

        self.assertIn("wf-123:0", tracer._spans)

    def test_end_task_removes_span(self):
        tracer = TracerOpenTelemetry(service_name="test")
        task = self._make_task()
        tracer.start_workflow(workflow_id="wf-123")
        tracer.start_task(task=task)

        tracer.end_task(task=task)

        self.assertNotIn("wf-123:0", tracer._spans)

    def test_end_task_failed_adds_exception_event(self):
        tracer = TracerOpenTelemetry(service_name="test")
        task = self._make_task(status=TypeStatus.FAILED)
        error = MagicMock()
        error.exception = "ValueError"
        error.message = "broken"
        task.errors = [error]

        tracer.start_workflow(workflow_id="wf-123")
        tracer.start_task(task=task)
        span = tracer._spans["wf-123:0"]

        tracer.end_task(task=task)

        span.add_event.assert_called_once()

    def test_end_workflow_not_started(self):
        tracer = TracerOpenTelemetry(service_name="test")

        tracer.end_workflow(workflow_id="nonexistent")

    def test_end_task_not_started(self):
        tracer = TracerOpenTelemetry(service_name="test")
        task = self._make_task()

        tracer.end_task(task=task)
