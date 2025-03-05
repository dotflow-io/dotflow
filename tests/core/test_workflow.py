"""Test context of controller"""

import unittest

from uuid import UUID
from unittest.mock import Mock
from types import FunctionType

from dotflow.core.workflow import Workflow
from dotflow.core.models import TypeExecution, TaskStatus
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.task import Task

from tests.mocks import (
    ActionStep,
    # ActionStepWithoutInit,
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
        controller = Workflow(tasks=self.tasks)

        self.assertListEqual(controller.tasks, self.tasks)
        self.assertIsInstance(controller.id, UUID)
        self.assertIsInstance(controller.success, FunctionType)
        self.assertIsInstance(controller.failure, FunctionType)

    def test_execution_with_function_completed(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )

        controller = Workflow(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TaskStatus.COMPLETED)

    def test_execution_with_function_failed(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )

        controller = Workflow(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TaskStatus.FAILED)

    def test_with_execution_mode_that_does_not_exist(self):
        with self.assertRaises(ExecutionModeNotExist):
            Workflow(tasks=self.tasks, mode="unknown")

    def test_with_execution_mode_sequential(self):
        Workflow(tasks=self.tasks, mode=TypeExecution.SEQUENTIAL)

    def test_with_execution_mode_background(self):
        Workflow(tasks=self.tasks, mode=TypeExecution.BACKGROUND)

    def test_with_execution_mode_parallel(self):
        Workflow(tasks=self.tasks, mode=TypeExecution.PARALLEL)

    def test_with_execution_mode_data_store(self):
        Workflow(tasks=self.tasks, mode=TypeExecution.DATA_STORE)

    def test_callback_success_called(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        mock_success = Mock()

        Workflow(tasks=[task], success=mock_success)
        mock_success.assert_called()

    def test_callback_failure_called(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )
        mock_failure = Mock()

        Workflow(tasks=[task], failure=mock_failure)
        mock_failure.assert_called()

    def test_execution_with_class_completed(self):
        task = Task(
            task_id=0,
            step=ActionStep,
            callback=simple_callback
        )

        controller = Workflow(tasks=[task])
        self.assertEqual(controller.tasks[0].status, TaskStatus.COMPLETED)
