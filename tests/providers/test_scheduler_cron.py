"""Test SchedulerCron"""

import sys
import threading
import unittest
from unittest.mock import MagicMock

from dotflow.abc.scheduler import Scheduler
from dotflow.core.types.overlap import TypeOverlap

mock_croniter = MagicMock()
sys.modules["croniter"] = mock_croniter

from dotflow.providers.scheduler_cron import SchedulerCron  # noqa: E402


class TestSchedulerCron(unittest.TestCase):
    def test_instance(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")

        self.assertIsInstance(scheduler, Scheduler)

    def test_default_overlap(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")

        self.assertEqual(scheduler.overlap, TypeOverlap.SKIP)

    def test_custom_overlap(self):
        scheduler = SchedulerCron(cron="*/5 * * * *", overlap="queue")

        self.assertEqual(scheduler.overlap, "queue")

    def test_cron_expression_stored(self):
        scheduler = SchedulerCron(cron="0 6 * * *")

        self.assertEqual(scheduler.cron, "0 6 * * *")

    def test_initial_state(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")

        self.assertFalse(scheduler.running)
        self.assertFalse(scheduler._executing)
        self.assertEqual(scheduler._queue_count, 0)

    def test_stop(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")
        scheduler.running = True

        scheduler.stop()

        self.assertFalse(scheduler.running)

    def test_dispatch_skip_when_executing(self):
        scheduler = SchedulerCron(cron="*/5 * * * *", overlap="skip")
        scheduler._executing = True
        workflow = MagicMock()

        scheduler._dispatch(workflow=workflow)

        workflow.assert_not_called()

    def test_dispatch_skip_when_idle(self):
        scheduler = SchedulerCron(cron="*/5 * * * *", overlap="skip")
        workflow = MagicMock()

        scheduler._dispatch(workflow=workflow)

        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join(timeout=2)

        workflow.assert_called_once()

    def test_dispatch_parallel(self):
        scheduler = SchedulerCron(cron="*/5 * * * *", overlap="parallel")
        scheduler._executing = True
        workflow = MagicMock()

        scheduler._dispatch(workflow=workflow)

        for t in threading.enumerate():
            if t != threading.current_thread():
                t.join(timeout=2)

        workflow.assert_called_once()

    def test_dispatch_queue_when_executing(self):
        scheduler = SchedulerCron(cron="*/5 * * * *", overlap="queue")
        scheduler._executing = True
        workflow = MagicMock()

        scheduler._dispatch(workflow=workflow)

        self.assertEqual(scheduler._queue_count, 1)
        workflow.assert_not_called()

    def test_execute_and_reset(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")
        scheduler._executing = True
        workflow = MagicMock()

        scheduler._execute_and_reset(workflow)

        workflow.assert_called_once()
        self.assertFalse(scheduler._executing)

    def test_handle_signal(self):
        scheduler = SchedulerCron(cron="*/5 * * * *")
        scheduler.running = True

        scheduler._handle_signal(signum=2, frame=None)

        self.assertFalse(scheduler.running)

    def test_run_stops_gracefully(self):
        from datetime import datetime, timedelta

        scheduler = SchedulerCron(cron="*/1 * * * *")
        workflow = MagicMock()

        def stop_and_return_next(*args, **kwargs):
            scheduler.stop()
            return datetime.now() + timedelta(seconds=0.01)

        mock_croniter_instance = MagicMock()
        mock_croniter_instance.get_next.side_effect = stop_and_return_next
        mock_croniter.croniter.return_value = mock_croniter_instance

        scheduler.start(workflow=workflow)

        self.assertFalse(scheduler.running)
