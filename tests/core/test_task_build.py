"""Test context of task build"""

import unittest

from dotflow.core.context import Context
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.action import Action as action
from dotflow.core.utils import callback


@action
def dummy_step():
    pass


class TestTaskBuild(unittest.TestCase):

    def setUp(self):
        self.example = {"foo": "bar"}

    def test_instantiating_class(self):
        task = TaskBuilder()

        self.assertListEqual(task.queu, [])

    def test_add_method(self):
        task = TaskBuilder()
        task.add(step=dummy_step)

        self.assertEqual(task.queu[0].task_id, 0)
        self.assertIsInstance(task.queu[0], Task)
        self.assertEqual(task.queu[0].callback, callback)
        self.assertEqual(len(task.queu), 1)

    def test_add_method_with_class_context(self):
        task = TaskBuilder()
        task.add(
            step=dummy_step,
            initial_context=Context(
                storage=self.example
            )
        )

        self.assertEqual(
            task.queu[0].initial_context.storage,
            self.example
        )

        self.assertIsInstance(
            task.queu[0].initial_context,
            Context
        )

    def test_add_method_without_class_context(self):
        task = TaskBuilder()
        task.add(
            step=dummy_step,
            initial_context=self.example
        )

        self.assertEqual(
            task.queu[0].initial_context.storage,
            self.example
        )

        self.assertIsInstance(
            task.queu[0].initial_context,
            Context
        )

    def test_count_method(self):
        task = TaskBuilder()

        initial_count = task.count()
        self.assertEqual(initial_count, 0)

        task.add(step=dummy_step)
        final_count = task.count()
        self.assertEqual(final_count, 1)
