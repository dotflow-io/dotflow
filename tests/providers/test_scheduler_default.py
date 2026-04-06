"""Test SchedulerDefault"""

import unittest
from unittest.mock import MagicMock

from dotflow.abc.scheduler import Scheduler
from dotflow.providers.scheduler_default import SchedulerDefault


class TestSchedulerDefault(unittest.TestCase):

    def test_instance(self):
        scheduler = SchedulerDefault()

        self.assertIsInstance(scheduler, Scheduler)

    def test_start_does_nothing(self):
        scheduler = SchedulerDefault()
        workflow = MagicMock()

        result = scheduler.start(workflow=workflow)

        self.assertIsNone(result)
        workflow.assert_not_called()

    def test_stop_does_nothing(self):
        scheduler = SchedulerDefault()

        result = scheduler.stop()

        self.assertIsNone(result)
