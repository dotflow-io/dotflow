"""Test EventBus and StatusChanged."""

import unittest
from unittest.mock import Mock

from dotflow.core.events import EventBus, StatusChanged


class TestEventBus(unittest.TestCase):
    def test_emit_runs_every_subscriber(self):
        bus = EventBus()

        a = Mock()
        b = Mock()

        bus.subscribe(a)
        bus.subscribe(b)
        bus.emit("payload")

        a.assert_called_once_with("payload")
        b.assert_called_once_with("payload")

    def test_subscriber_failure_does_not_block_others(self):
        bus = EventBus()

        bus.subscribe(Mock(side_effect=RuntimeError("boom")))
        survivor = Mock()
        bus.subscribe(survivor)

        bus.emit("payload")

        survivor.assert_called_once_with("payload")

    def test_subscribers_run_in_registration_order(self):
        bus = EventBus()
        calls = []

        bus.subscribe(lambda _e: calls.append("a"))
        bus.subscribe(lambda _e: calls.append("b"))
        bus.subscribe(lambda _e: calls.append("c"))

        bus.emit("x")

        self.assertEqual(calls, ["a", "b", "c"])


class TestStatusChanged(unittest.TestCase):
    def test_carries_task_old_new(self):
        event = StatusChanged(task="t", old="OLD", new="NEW")

        self.assertEqual(event.task, "t")
        self.assertEqual(event.old, "OLD")
        self.assertEqual(event.new, "NEW")
