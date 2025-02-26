"""Test context of task"""

import unittest

from dotflow.core.context import Context
from dotflow.core.task import Task

from tests.mocks import (
    action_step,
    simple_callback
)


class TestTask(unittest.TestCase):

    def setUp(self):
        self.example = {"foo": "bar"}

    def test_instantiating_class(self):
        Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=action_step,
            callback=simple_callback
        )

    def test_task_id(self):
        task = Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=action_step,
            callback=simple_callback
        )

        self.assertEqual(task.task_id, 0)

    def test_initial_context(self):
        task = Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=action_step,
            callback=simple_callback
        )

        self.assertEqual(
            task.initial_context.storage,
            self.example
        )
