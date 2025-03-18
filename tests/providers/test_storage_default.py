"""Test StorageFile"""

import unittest

from uuid import uuid4

from dotflow.core.task import Task
from dotflow.core.context import Context
from dotflow.providers.storage_default import StorageDefault

from tests.mocks import action_step


class TestStorageDefault(unittest.TestCase):

    def test_storage_default_instance(self):
        StorageDefault()

    def test_get(self):
        expected_value = "flow"

        task = Task(
            task_id=0,
            workflow_id=uuid4(),
            step=action_step,
        )
        task.current_context = expected_value

        storage = StorageDefault()
        result = storage.get(key=storage.key(task=task))

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, expected_value)
