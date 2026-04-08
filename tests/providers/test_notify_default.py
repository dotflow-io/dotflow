"""Test NotifyDefault"""

import unittest
from unittest.mock import MagicMock

from dotflow.abc.notify import Notify
from dotflow.providers.notify_default import NotifyDefault


class TestNotifyDefault(unittest.TestCase):
    def test_instance(self):
        notify = NotifyDefault()

        self.assertIsInstance(notify, Notify)

    def test_hook_status_task_does_nothing(self):
        notify = NotifyDefault()
        task = MagicMock()

        result = notify.hook_status_task(task=task)

        self.assertIsNone(result)
