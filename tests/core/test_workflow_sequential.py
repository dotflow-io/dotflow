"""Test context of controller"""

import unittest

from uuid import uuid4
from unittest.mock import Mock

from dotflow.core.workflow import Sequential, grouper
from dotflow.core.types import TypeStatus
from dotflow.core.task import Task, TaskError

from tests.mocks import (
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestWorkflowSequential(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()
        self.ignore = False

    def test_instantiating_sequential_class(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = Sequential(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        self.assertListEqual(execution.tasks, tasks)
        self.assertDictEqual(execution.groups, groups)
        self.assertEqual(execution.workflow_id, self.workflow_id)
        self.assertEqual(execution.ignore, self.ignore)

    def test_workflow_with_callback(self):
        mock_callback = Mock()
        tasks = [Task(task_id=0, step=action_step, callback=mock_callback)]

        Sequential(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        mock_callback.assert_called()

    def test_workflow_with_function_completed(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]

        execution = Sequential(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        self.assertEqual(execution.tasks[0].status, TypeStatus.COMPLETED)
        self.assertEqual(execution.tasks[0].current_context.storage, {"foo": "bar"})
        self.assertIsInstance(execution.tasks[0].error, TaskError)
        self.assertEqual(execution.tasks[0].error.message, "")

    def test_workflow_with_function_failed(self):
        tasks = [Task(task_id=0, step=action_step_with_error, callback=simple_callback)]

        execution = Sequential(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        self.assertEqual(execution.tasks[0].status, TypeStatus.FAILED)
        self.assertIsNone(execution.tasks[0].current_context.storage)
        self.assertIsInstance(execution.tasks[0].error, TaskError)
        self.assertEqual(execution.tasks[0].error.message, "Fail!")

    def test_instantiating_sequential_setup_queue(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = Sequential(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()

        self.assertListEqual(execution.queue, [])

    def test_instantiating_sequential_flow_callback(self):
        task = Task(task_id=5, step=action_step, callback=simple_callback)
        groups = grouper(tasks=[task])

        execution = Sequential(
            tasks=[task],
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()
        execution._flow_callback(task=task)

        tasks = execution.get_tasks()
        self.assertEqual(tasks[0].task_id, 5)
