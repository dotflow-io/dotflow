"""Test context of controller"""

import unittest

from uuid import UUID
from unittest.mock import Mock
from types import FunctionType

from dotflow.core.workflow import Manager
from dotflow.core.types import ExecutionModeType, StatusTaskType
from dotflow.core.exception import ExecutionModeNotExist
from dotflow.core.task import Task, QueueGroup
from dotflow.core.plugin import Plugin

from tests.mocks import (
    ActionStep,
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.plugins = Plugin()
        self.group = QueueGroup()
        self.group.add(
                item=Task(
                    task_id=0,
                    step=action_step,
                    plugins=self.plugins,
                    callback=simple_callback
                )
        )

    def test_instantiating_workflow_class(self):
        controller = Manager(
            group=self.group,
            plugins=self.plugins
        )

        self.assertEqual(controller.group, self.group)
        self.assertIsInstance(controller.workflow_id, UUID)
        self.assertIsInstance(controller.on_success, FunctionType)
        self.assertIsInstance(controller.on_failure, FunctionType)

    def test_workflow_with_function_success(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step,
                plugins=self.plugins,
                callback=simple_callback
            )
        )

        controller = Manager(
            group=group,
            plugins=self.plugins
        )
        self.assertEqual(controller.group.tasks()[0].status, StatusTaskType.SUCCESS)

    def test_workflow_with_function_failed(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step_with_error,
                plugins=self.plugins,
                callback=simple_callback
            )
        )

        controller = Manager(
            group=group,
            plugins=self.plugins
        )
        self.assertEqual(controller.group.tasks()[0].status, StatusTaskType.FAILED)

    def test_with_execution_mode_that_does_not_exist(self):
        with self.assertRaises(ExecutionModeNotExist):
            Manager(
                group=self.group,
                mode="unknown",
                plugins=self.plugins
            )

    def test_with_execution_mode_sequential(self):
        Manager(
            group=self.group,
            mode=ExecutionModeType.SEQUENTIAL,
            plugins=self.plugins
        )

    def test_with_execution_mode_background(self):
        Manager(
            group=self.group,
            mode=ExecutionModeType.BACKGROUND,
            plugins=self.plugins
        )

    def test_with_execution_mode_parallel(self):
        Manager(
            group=self.group,
            mode=ExecutionModeType.PARALLEL,
            plugins=self.plugins
        )

    def test_callback_success_called(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step,
                plugins=self.plugins,
                callback=simple_callback
            )
        )
        mock_success = Mock()

        Manager(
            group=group,
            on_success=mock_success,
            plugins=self.plugins
        )
        mock_success.assert_called()

    def test_callback_failure_called(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step_with_error,
                plugins=self.plugins,
                callback=simple_callback
            )
        )
        mock_failure = Mock()

        Manager(
            group=group,
            on_failure=mock_failure,
            plugins=self.plugins
        )
        mock_failure.assert_called()

    def test_workflow_with_class_success(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=ActionStep,
                plugins=self.plugins,
                callback=simple_callback
            )
        )

        controller = Manager(
            group=group,
            plugins=self.plugins
        )
        self.assertEqual(controller.group.tasks()[0].status, StatusTaskType.SUCCESS)
