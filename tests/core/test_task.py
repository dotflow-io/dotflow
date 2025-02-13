import unittest

from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.actions import action


@action
def dummy_step():
    pass


def dummy_callback(*args, **kwargs):
    pass


class TestTask(unittest.TestCase):

    def setUp(self):
        self.example = {"foo": "bar"}

    def test_instantiating_class(self):
        Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=dummy_step,
            callback=dummy_callback
        )

    def test_task_id(self):
        task = Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=dummy_step,
            callback=dummy_callback
        )

        self.assertEqual(task.task_id, 0)

    def test_initial_context(self):
        task = Task(
            task_id=0,
            initial_context=Context(
                storage=self.example
            ),
            step=dummy_step,
            callback=dummy_callback
        )

        self.assertEqual(
            task.initial_context.storage,
            self.example
        )
