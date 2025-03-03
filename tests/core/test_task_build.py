"""Test context of task build"""

import unittest

from dotflow.core.context import Context
from dotflow.core.exception import MissingActionDecorator
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.utils import basic_callback

from tests.mocks import (
    action_step,
    simple_step,
    SimpleStep
)


class TestTaskBuild(unittest.TestCase):

    def setUp(self):
        self.content = {"foo": "bar"}

    def test_instantiating_class(self):
        task = TaskBuilder()

        self.assertListEqual(task.queu, [])

    def test_add_method(self):
        task = TaskBuilder()
        task.add(step=action_step)

        self.assertEqual(task.queu[0].task_id, 0)
        self.assertIsInstance(task.queu[0], Task)
        self.assertEqual(task.queu[0].callback, basic_callback)
        self.assertEqual(len(task.queu), 1)

    def test_add_method_with_class_context(self):
        task = TaskBuilder()
        task.add(
            step=action_step,
            initial_context=Context(
                storage=self.content
            )
        )

        self.assertEqual(
            task.queu[0].initial_context.storage,
            self.content
        )

        self.assertIsInstance(
            task.queu[0].initial_context,
            Context
        )

    def test_add_method_without_class_context(self):
        task = TaskBuilder()
        task.add(
            step=action_step,
            initial_context=self.content
        )

        self.assertEqual(
            task.queu[0].initial_context.storage,
            self.content
        )

        self.assertIsInstance(
            task.queu[0].initial_context,
            Context
        )

    def test_count_method(self):
        task = TaskBuilder()

        initial_count = 0
        final_count = 1

        self.assertEqual(task.count(), initial_count)

        task.add(step=action_step)

        self.assertEqual(task.count(), final_count)

    def test_clear_method(self):
        task = TaskBuilder()

        expected_count_before = 1
        expected_count_after = 0

        task.add(step=action_step)
        self.assertEqual(task.count(), expected_count_before)

        task.clear()

        self.assertEqual(task.count(), expected_count_after)

    def test_with_method_step_without_decorator(self):
        task = TaskBuilder()

        with self.assertRaises(MissingActionDecorator):
            task.add(step=simple_step)

    def test_with_class_step_without_decorator(self):
        task = TaskBuilder()

        with self.assertRaises(MissingActionDecorator):
            task.add(step=SimpleStep)
