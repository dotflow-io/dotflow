"""Test context of controller"""

import unittest

from uuid import UUID
from unittest.mock import Mock
from types import FunctionType

from dotflow.core.controller import Controller
from dotflow.core.models import Execution, Status 
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.task import Task

from tests.mocks import (
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestController(unittest.TestCase):

    def setUp(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        self.tasks = [task]

    def test_instantiating_class(self):
        controller = Controller(tasks=self.tasks)

        self.assertListEqual(controller.tasks, self.tasks)
        self.assertIsInstance(controller.workflow_id, UUID)
        self.assertIsInstance(controller.success, FunctionType)
        self.assertIsInstance(controller.failure, FunctionType)

    def test_function_execution_completed(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )

        controller = Controller(tasks=[task])
        self.assertEqual(controller.tasks[0].status, Status.COMPLETED)

    def test_function_execution_failed(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )

        controller = Controller(tasks=[task])
        self.assertEqual(controller.tasks[0].status, Status.FAILED)

    def test_with_execution_mode_that_does_not_exist(self):
        with self.assertRaises(ExecutionModeNotExist):
            Controller(tasks=self.tasks, mode="unknown")

    def test_with_execution_mode_sequential(self):
        Controller(tasks=self.tasks, mode=Execution.SEQUENTIAL)

    def test_with_execution_mode_background(self):
        Controller(tasks=self.tasks, mode=Execution.BACKGROUND)

    def test_with_execution_mode_parallel(self):
        Controller(tasks=self.tasks, mode=Execution.PARALLEL)

    def test_with_execution_mode_data_store(self):
        Controller(tasks=self.tasks, mode=Execution.DATA_STORE)

    def test_callback_success_called(self):
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        mock_success = Mock()

        Controller(tasks=[task], success=mock_success)
        mock_success.assert_called()

    def test_callback_failure_called(self):
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )
        mock_failure = Mock()

        Controller(tasks=[task], failure=mock_failure)
        mock_failure.assert_called()
