"""Test MetricsDefault"""

import unittest
from unittest.mock import MagicMock

from dotflow.abc.metrics import Metrics
from dotflow.providers.metrics_default import MetricsDefault


class TestMetricsDefault(unittest.TestCase):

    def test_instance(self):
        metrics = MetricsDefault()

        self.assertIsInstance(metrics, Metrics)

    def test_workflow_started_does_nothing(self):
        metrics = MetricsDefault()

        result = metrics.workflow_started(workflow_id="wf-1")

        self.assertIsNone(result)

    def test_workflow_completed_does_nothing(self):
        metrics = MetricsDefault()

        result = metrics.workflow_completed(workflow_id="wf-1", duration=1.5)

        self.assertIsNone(result)

    def test_workflow_failed_does_nothing(self):
        metrics = MetricsDefault()

        result = metrics.workflow_failed(workflow_id="wf-1", duration=1.5)

        self.assertIsNone(result)

    def test_task_completed_does_nothing(self):
        metrics = MetricsDefault()
        task = MagicMock()

        result = metrics.task_completed(task=task)

        self.assertIsNone(result)

    def test_task_failed_does_nothing(self):
        metrics = MetricsDefault()
        task = MagicMock()

        result = metrics.task_failed(task=task)

        self.assertIsNone(result)

    def test_task_retried_does_nothing(self):
        metrics = MetricsDefault()
        task = MagicMock()

        result = metrics.task_retried(task=task)

        self.assertIsNone(result)
