"""Test context of execution"""

import unittest

from uuid import uuid4
from functools import partial
from types import FunctionType

from dotflow.core.action import Action as action
from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.task import Task
from dotflow.core.plugin import Plugin

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
        self.workflow_id = uuid4()
        self.plugins = Plugin()
        self.task = partial(
            Task,
            task_id=0,
            workflow_id=self.workflow_id,
            callback=simple_callback,
            plugins=self.plugins
        )

    def test_execution_result_str(self):
        controller = Execution(
            task=self.task(step=task_str, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, "")
        self.assertIsInstance(controller.task.current_context.storage, str)

    def test_execution_result_int(self):
        controller = Execution(
            task=self.task(step=task_int, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, 1)
        self.assertIsInstance(controller.task.current_context.storage, int)

    def test_execution_result_float(self):
        controller = Execution(
            task=self.task(step=task_float, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, 1.0)
        self.assertIsInstance(controller.task.current_context.storage, float)

    def test_execution_result_dict(self):
        controller = Execution(
            task=self.task(step=task_dict, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, {})
        self.assertIsInstance(controller.task.current_context.storage, dict)

    def test_execution_result_list(self):
        controller = Execution(
            task=self.task(step=task_list, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, [])
        self.assertIsInstance(controller.task.current_context.storage, list)

    def test_execution_result_tuple(self):
        controller = Execution(
            task=self.task(step=task_tuple, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertEqual(controller.task.current_context.storage, ())
        self.assertIsInstance(controller.task.current_context.storage, tuple)

    def test_execution_result_function(self):
        controller = Execution(
            task=self.task(step=task_function, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertIsInstance(controller.task.current_context.storage, FunctionType)

    def test_execution_result_class(self):
        controller = Execution(
            task=self.task(step=task_class, workflow_id=self.workflow_id),
            workflow_id=self.workflow_id,
            previous_context=Context()
        )
        self.assertIsInstance(controller.task.current_context.storage, Inside)
