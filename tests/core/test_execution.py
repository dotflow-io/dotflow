"""Test context of execution"""

import unittest

from uuid import uuid4

from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.models import Status
from dotflow.core.task import Task

from tests.mocks import (
    ActionStep,
    ActionStepWithError,
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestExecution(unittest.TestCase):

    def test_execution_with_function_completed(self):
        workflow_id = uuid4()
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=workflow_id,
            previous_context=Context()
        )

        self.assertEqual(controller.task.status, Status.COMPLETED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_function_failed(self):
        workflow_id = uuid4()
        task = Task(
            task_id=0,
            step=action_step_with_error,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=workflow_id,
            previous_context=Context()
        )

        self.assertEqual(controller.task.status, Status.FAILED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_class_completed(self):
        workflow_id = uuid4()
        task = Task(
            task_id=0,
            step=ActionStep,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=workflow_id,
            previous_context=Context()
        )

        self.assertEqual(controller.task.status, Status.COMPLETED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_class_failed(self):
        workflow_id = uuid4()
        task = Task(
            task_id=0,
            step=ActionStepWithError,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=workflow_id,
            previous_context=Context()
        )

        self.assertEqual(controller.task.status, Status.FAILED)
        self.assertEqual(controller.task.workflow_id, workflow_id)
