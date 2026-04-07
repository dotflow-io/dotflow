"""Test TracerDefault"""

import unittest
from unittest.mock import MagicMock

from dotflow.abc.tracer import Tracer
from dotflow.providers.tracer_default import TracerDefault


class TestTracerDefault(unittest.TestCase):

    def test_instance(self):
        tracer = TracerDefault()

        self.assertIsInstance(tracer, Tracer)

    def test_start_workflow_does_nothing(self):
        tracer = TracerDefault()

        result = tracer.start_workflow(workflow_id="wf-1")

        self.assertIsNone(result)

    def test_end_workflow_does_nothing(self):
        tracer = TracerDefault()

        result = tracer.end_workflow(workflow_id="wf-1")

        self.assertIsNone(result)

    def test_start_task_does_nothing(self):
        tracer = TracerDefault()
        task = MagicMock()

        result = tracer.start_task(task=task)

        self.assertIsNone(result)

    def test_end_task_does_nothing(self):
        tracer = TracerDefault()
        task = MagicMock()

        result = tracer.end_task(task=task)

        self.assertIsNone(result)
