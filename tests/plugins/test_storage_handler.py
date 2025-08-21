"""Test StorageFile"""

import unittest

from uuid import uuid4

from dotflow.core.task import Task
from dotflow.core.context import Context
from dotflow.core.plugin import Plugin
from dotflow.plugins.storage import StorageHandler

from tests.mocks import action_step


class TestStorageHandler(unittest.TestCase):

    def setUp(self):
        self.plugins = Plugin()

    def test_storage_default_instance(self):
        StorageHandler()

    def test_get(self):
        expected_value = "flow"

        task = Task(
            task_id=0,
            workflow_id=uuid4(),
            plugins=self.plugins,
            step=action_step,
        )
        task.current_context = expected_value

        storage = StorageHandler()
        result = storage.get(key=storage.key(task=task))

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value)
