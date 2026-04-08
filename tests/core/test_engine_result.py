"""Test context of execution result"""

import unittest
from functools import partial
from types import FunctionType
from uuid import uuid4

from dotflow.core.action import Action as action
from dotflow.core.context import Context
from dotflow.core.engine import TaskEngine
from dotflow.core.task import Task
from tests.mocks import simple_callback


def inside():
    pass


class Inside:
    def __init__(self):
        pass


@action
def task_str():
    return ""


@action
def task_int():
    return 1


@action
def task_float():
    return 1.0


@action
def task_dict():
    return {}


@action
def task_list():
    return []


@action
def task_tuple():
    return ()


@action
def task_function():
    return inside


@action
def task_class():
    return Inside()


class TestExecutionResult(unittest.TestCase):
    def setUp(self):
        self.task = partial(Task, task_id=0, callback=simple_callback)
        self.workflow_id = uuid4()

    def _run(self, step):
        task = self.task(step=step)
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )
        with engine.start():
            engine.execute()
        return task

    def test_execution_result_str(self):
        task = self._run(task_str)
        self.assertEqual(task.current_context.storage, "")
        self.assertIsInstance(task.current_context.storage, str)

    def test_execution_result_int(self):
        task = self._run(task_int)
        self.assertEqual(task.current_context.storage, 1)
        self.assertIsInstance(task.current_context.storage, int)

    def test_execution_result_float(self):
        task = self._run(task_float)
        self.assertEqual(task.current_context.storage, 1.0)
        self.assertIsInstance(task.current_context.storage, float)

    def test_execution_result_dict(self):
        task = self._run(task_dict)
        self.assertEqual(task.current_context.storage, {})
        self.assertIsInstance(task.current_context.storage, dict)

    def test_execution_result_list(self):
        task = self._run(task_list)
        self.assertEqual(task.current_context.storage, [])
        self.assertIsInstance(task.current_context.storage, list)

    def test_execution_result_tuple(self):
        task = self._run(task_tuple)
        self.assertEqual(task.current_context.storage, ())
        self.assertIsInstance(task.current_context.storage, tuple)

    def test_execution_result_function(self):
        task = self._run(task_function)
        self.assertIsInstance(task.current_context.storage, FunctionType)

    def test_execution_result_class(self):
        task = self._run(task_class)
        self.assertIsInstance(task.current_context.storage, Inside)
