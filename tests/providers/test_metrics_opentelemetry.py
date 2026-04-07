"""Test MetricsOpenTelemetry"""

import sys
import unittest
from unittest.mock import MagicMock

from dotflow.abc.metrics import Metrics
from dotflow.core.types.status import TypeStatus

mock_otel_metrics = MagicMock()
sys.modules["opentelemetry"] = MagicMock()
sys.modules["opentelemetry.metrics"] = mock_otel_metrics
sys.modules["opentelemetry.sdk"] = MagicMock()
sys.modules["opentelemetry.sdk.metrics"] = MagicMock()
sys.modules["opentelemetry.sdk.resources"] = MagicMock()

from dotflow.providers.metrics_opentelemetry import MetricsOpenTelemetry  # noqa: E402


class TestMetricsOpenTelemetry(unittest.TestCase):

    def _make_task(self, status=TypeStatus.COMPLETED):
        task = MagicMock()
        task.status = status
        task.workflow_id = "wf-123"
        task.task_id = 0
        task.duration = 0.5
        task.retry_count = 1
        return task

    def test_instance(self):
        metrics = MetricsOpenTelemetry(service_name="test")

        self.assertIsInstance(metrics, Metrics)

    def test_workflow_started(self):
        metrics = MetricsOpenTelemetry(service_name="test")

        metrics.workflow_started(workflow_id="wf-1")

        metrics._workflow_total.add.assert_called_with(1, {"status": "started"})

    def test_workflow_completed(self):
        metrics = MetricsOpenTelemetry(service_name="test")

        metrics.workflow_completed(workflow_id="wf-1", duration=2.5)

        metrics._workflow_total.add.assert_called_with(1, {"status": "completed"})
        metrics._workflow_duration.record.assert_called_with(2.5, {"status": "completed"})

    def test_workflow_failed(self):
        metrics = MetricsOpenTelemetry(service_name="test")

        metrics.workflow_failed(workflow_id="wf-1", duration=1.0)

        metrics._workflow_total.add.assert_called_with(1, {"status": "failed"})
        metrics._workflow_duration.record.assert_called_with(1.0, {"status": "failed"})

    def test_task_completed(self):
        metrics = MetricsOpenTelemetry(service_name="test")
        task = self._make_task()

        metrics.task_completed(task=task)

        metrics._task_total.add.assert_called_with(1, {"status": "completed"})
        metrics._task_duration.record.assert_called_with(0.5, {"status": "completed"})

    def test_task_failed(self):
        metrics = MetricsOpenTelemetry(service_name="test")
        task = self._make_task(status=TypeStatus.FAILED)

        metrics.task_failed(task=task)

        metrics._task_total.add.assert_called_with(1, {"status": "failed"})

    def test_task_retried(self):
        metrics = MetricsOpenTelemetry(service_name="test")
        task = self._make_task()

        metrics.task_retried(task=task)

        metrics._task_retry_total.add.assert_called_with(1)
