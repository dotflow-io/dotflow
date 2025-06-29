"""Test context of controller"""

import unittest

from uuid import UUID
from unittest.mock import Mock
from types import FunctionType

from dotflow.core.workflow import Manager
from dotflow.core.types import TypeExecution, TypeStatus
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.task import Task

from tests.mocks import (
    ActionStep,
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        self.tasks = [task]

    def test_instantiating_workflow_class(self):
        controller = Manager(tasks=self.tasks)

        self.assertListEqual(controller.tasks, self.tasks)
        self.assertIsInstance(controller.workflow_id, UUID)
        self.assertIsInstance(controller.on_success, FunctionType)
        self.assertIsInstance(controller.on_failure, FunctionType)

    def test_workflow_with_function_completed(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )

        controller = Manager(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TypeStatus.COMPLETED)

    def test_workflow_with_function_failed(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )

        controller = Manager(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TypeStatus.FAILED)

    def test_with_execution_mode_that_does_not_exist(self):
        with self.assertRaises(ExecutionModeNotExist):
            Manager(tasks=self.tasks, mode="unknown")

    def test_with_execution_mode_sequential(self):
        Manager(tasks=self.tasks, mode=TypeExecution.SEQUENTIAL)

    def test_with_execution_mode_background(self):
        Manager(tasks=self.tasks, mode=TypeExecution.BACKGROUND)

    def test_with_execution_mode_parallel(self):
        Manager(tasks=self.tasks, mode=TypeExecution.PARALLEL)

    def test_callback_success_called(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        mock_success = Mock()

        Manager(tasks=[task], on_success=mock_success)
        mock_success.assert_called()

    def test_callback_failure_called(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )
        mock_failure = Mock()

        Manager(tasks=[task], on_failure=mock_failure)
        mock_failure.assert_called()

    def test_workflow_with_class_completed(self):
        task = Task(
            task_id=0,
            step=ActionStep,
            callback=simple_callback
        )

        controller = Manager(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TypeStatus.COMPLETED)
