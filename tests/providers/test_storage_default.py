"""Test StorageDefault"""

import unittest
from uuid import uuid4

from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.providers.storage_default import StorageDefault
from tests.mocks import action_step


class TestStorageDefault(unittest.TestCase):
    def test_storage_default_instance(self):
        StorageDefault()

    def test_post_and_get_roundtrip(self):
        storage = StorageDefault()
        context = Context(storage={"data": 42})

        storage.post(key="test-key", context=context)
        result = storage.get(key="test-key")

        self.assertIsInstance(result, Context)
        self.assertEqual(result.storage, {"data": 42})

    def test_get_missing_key_returns_empty_context(self):
        storage = StorageDefault()
        result = storage.get(key="nonexistent")

        self.assertIsInstance(result, Context)
        self.assertIsNone(result.storage)

    def test_key_format(self):
        task = Task(
            task_id=0,
            workflow_id=uuid4(),
            step=action_step,
        )

        storage = StorageDefault()
        key = storage.key(task=task)

        self.assertEqual(key, f"{task.workflow_id}-{task.task_id}")

    def test_get_with_task_context(self):
        task = Task(
            task_id=0,
            workflow_id=uuid4(),
            step=action_step,
        )
        task.current_context = "flow"

        storage = StorageDefault()
        key = storage.key(task=task)
        result = storage.get(key=key)

        self.assertIsInstance(result, Context)
