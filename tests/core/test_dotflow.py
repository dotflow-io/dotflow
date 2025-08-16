"""Test context of workflow"""

import unittest

from dotflow.core.workflow import Manager
from dotflow.core.context import Context
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.dotflow import DotFlow
from dotflow.core.types.status import TypeStatus

from tests.mocks import action_step


class TestDotFlow(unittest.TestCase):

    def setUp(self):
        self.workflow = DotFlow()
        self.workflow.add(step=action_step)

    def test_instantiating_dotflow_class(self):
        self.assertIsInstance(self.workflow.task, TaskBuilder)
        self.assertIsInstance(self.workflow.start(), Manager)

    def test_result_task_with_start(self):
        self.workflow.start()
        result = self.workflow.result_task()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Task)
        self.assertEqual(result[0].status, TypeStatus.COMPLETED)

    def test_result_context_with_start(self):
        self.workflow.start()
        result = self.workflow.result_context()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Context)

    def test_result_storage_with_start(self):
        self.workflow.start()
        result = self.workflow.result_storage()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {"foo": "bar"})

    def test_result_task_without_start(self):
        result = self.workflow.result_task()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Task)
        self.assertEqual(result[0].status, TypeStatus.NOT_STARTED)

    def test_result_context_without_start(self):
        result = self.workflow.result_context()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Context)

    def test_result_storage_without_start(self):
        result = self.workflow.result_storage()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], None)
