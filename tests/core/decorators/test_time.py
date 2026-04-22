"""Test time decorator"""

import unittest

from dotflow.core.decorators.time import time
from dotflow.core.task import Task
from tests.mocks import action_step, simple_callback


class TestTimeDecorator(unittest.TestCase):
    def test_duration_is_set_after_execution(self):
        @time
        def run():
            return Task(
                task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
                step=action_step,
                callback=simple_callback,
            )

        task = run()

        self.assertIsNotNone(task.duration)

    def test_duration_is_positive(self):
        @time
        def run():
            return Task(
                task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
                step=action_step,
                callback=simple_callback,
            )

        task = run()

        self.assertGreaterEqual(task.duration, 0)

    def test_return_value_is_preserved(self):
        expected_task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step,
            callback=simple_callback,
        )

        @time
        def run():
            return expected_task

        result = run()

        self.assertIs(result, expected_task)

    def test_duration_is_float(self):
        @time
        def run():
            return Task(
                task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
                step=action_step,
                callback=simple_callback,
            )

        task = run()

        self.assertIsInstance(task.duration, float)
