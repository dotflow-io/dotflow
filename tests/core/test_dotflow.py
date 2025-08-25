"""Test of dotflow"""

import unittest

from uuid import UUID

from dotflow.core.workflow import Manager
from dotflow.core.context import Context
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.dotflow import DotFlow, DotflowInstance
from dotflow.core.types.task import StatusTaskType
from dotflow.core.plugin import Plugin

from tests.mocks import action_step


class TestDotflowInstance(unittest.TestCase):

    def setUp(self):
        self.instance = DotflowInstance()

    def test_instantiating_dotflow_instance_class(self):
        self.assertIsNone(self.instance._plugins)
        self.assertIsNone(self.instance._workflow_id)
        self.assertIsNone(self.instance._task)
        self.assertIsNone(self.instance._add)
        self.assertIsNone(self.instance._start)


class TestDotFlow(unittest.TestCase):

    def setUp(self):
        self.dotflow = DotFlow()
        self.dotflow.add(step=action_step)
        self.index = 0
        self.size = 1

    def test_instantiating_dotflow_class(self):
        self.assertIsInstance(self.dotflow.plugins, Plugin)
        self.assertIsInstance(self.dotflow.workflow_id, UUID)
        self.assertIsInstance(self.dotflow.task, TaskBuilder)
        self.assertIsInstance(self.dotflow.start(), Manager)

    def test_result_task_with_start(self):
        self.dotflow.start()
        result = self.dotflow.result_task()

        self.assertEqual(len(result), self.size)
        self.assertIsInstance(result[self.index], Task)
        self.assertEqual(result[self.index].status, StatusTaskType.SUCCESS)

    def test_result_context_with_start(self):
        self.dotflow.start()
        result = self.dotflow.result_context()

        self.assertEqual(len(result), self.size)
        self.assertIsInstance(result[self.index], Context)

    def test_result_storage_with_start(self):
        self.dotflow.start()
        result = self.dotflow.result_storage()

        self.assertEqual(len(result), self.size)
        self.assertEqual(result[self.index], {"foo": "bar"})

    def test_result_task_without_start(self):
        result = self.dotflow.result_task()

        self.assertEqual(len(result), self.size)
        self.assertIsInstance(result[self.index], Task)
        self.assertEqual(result[self.index].status, StatusTaskType.IN_QUEUE)

    def test_result_context_without_start(self):
        result = self.dotflow.result_context()

        self.assertEqual(len(result), self.size)
        self.assertIsInstance(result[self.index], Context)

    def test_result_storage_without_start(self):
        result = self.dotflow.result_storage()

        self.assertEqual(len(result), self.size)
        self.assertEqual(result[self.index], None)

    def test_dotflow_plugins_object(self):
        self.assertIsNotNone(self.dotflow.plugins)
        self.assertFalse(callable(self.dotflow.plugins))

    def test_dotflow_workflow_id_object(self):
        self.assertIsNotNone(self.dotflow.workflow_id)
        self.assertFalse(callable(self.dotflow.workflow_id))

    def test_dotflow_task_object(self):
        self.assertIsNotNone(self.dotflow.task)
        self.assertFalse(callable(self.dotflow.task))

    def test_dotflow_add_object(self):
        self.assertIsNotNone(self.dotflow.add)
        self.assertTrue(callable(self.dotflow.add))

    def test_dotflow_start_object(self):
        self.assertIsNotNone(self.dotflow.start)
        self.assertTrue(callable(self.dotflow.start))
