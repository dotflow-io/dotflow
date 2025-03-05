"""Test context of execution"""

import unittest

from uuid import uuid4

from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.types import TaskStatus
from dotflow.core.task import Task

from tests.mocks import (
    ActionStep,
    ActionStepWithInitialContext,
    ActionStepWithPreviousContext,
    ActionStepWithContexts,
    ActionStepWithError,
    action_step,
    action_step_with_initial_context,
    action_step_with_previous_context,
    action_step_with_contexts,
    action_step_with_error,
    simple_callback,
)


class TestExecution(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()
        self.context = {"context": True}

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

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
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

        self.assertEqual(controller.task.status, TaskStatus.FAILED)
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

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
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

        self.assertEqual(controller.task.status, TaskStatus.FAILED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_function_with_initial_context(self):
        task = Task(
            task_id=0,
            step=action_step_with_initial_context,
            callback=simple_callback,
            initial_context=self.context
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=None
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)

    def test_execution_function_with_previous_context(self):
        task = Task(
            task_id=0,
            step=action_step_with_previous_context,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task._previous_context.storage, self.context)

    def test_execution_function_with_contexts(self):
        task = Task(
            task_id=0,
            step=action_step_with_contexts,
            callback=simple_callback,
            initial_context=self.context
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)
        self.assertEqual(controller.task.previous_context.storage, self.context)

    def test_execution_class_with_initial_context(self):
        task = Task(
            task_id=0,
            step=ActionStepWithInitialContext,
            callback=simple_callback,
            initial_context=self.context
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=None
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)

    def test_execution_class_with_previous_context(self):
        task = Task(
            task_id=0,
            step=ActionStepWithPreviousContext,
            callback=simple_callback
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task._previous_context.storage, self.context)

    def test_execution_class_with_contexts(self):
        task = Task(
            task_id=0,
            step=ActionStepWithContexts,
            callback=simple_callback,
            initial_context=self.context
        )
        controller = Execution(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context
        )

        self.assertEqual(controller.task.status, TaskStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)
        self.assertEqual(controller.task.previous_context.storage, self.context)
