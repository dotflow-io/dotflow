"""Test context of controller"""

import unittest

from uuid import uuid4
from unittest.mock import Mock

from dotflow.core.workflow import Sequential
from dotflow.core.types import StatusTaskType
from dotflow.core.task import Task, TaskError, QueueGroup
from dotflow.core.plugin import Plugin

from tests.mocks import (
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestWorkflowSequential(unittest.TestCase):

    def setUp(self):
        self.plugins = Plugin()
        self.workflow_id = uuid4()
        self.ignore = False

    def test_instantiating_sequential_class(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step,
                plugins=self.plugins,
                callback=simple_callback
            )
        )

        execution = Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )

        self.assertIsInstance(execution.group, QueueGroup)
        self.assertEqual(execution.workflow_id, self.workflow_id)
        self.assertEqual(execution.ignore, self.ignore)

    def test_workflow_with_callback(self):
        mock_callback = Mock()
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step,
                plugins=self.plugins,
                callback=mock_callback
            )
        )

        Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )

        mock_callback.assert_called()

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

        execution = Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )
        tasks = execution.group.tasks()

        self.assertEqual(tasks[0].status, StatusTaskType.SUCCESS)
        self.assertEqual(tasks[0].current_context.storage, {"foo": "bar"})
        self.assertIsInstance(tasks[0].error, TaskError)
        self.assertEqual(tasks[0].error.message, "")

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

        execution = Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )
        tasks = execution.group.tasks()

        self.assertEqual(tasks[0].status, StatusTaskType.FAILED)
        self.assertIsNone(tasks[0].current_context.storage)
        self.assertIsInstance(tasks[0].error, TaskError)
        self.assertEqual(tasks[0].error.message, "Fail!")

    def test_instantiating_sequential_setup_queue(self):
        group = QueueGroup()
        group.add(
            item=Task(
                task_id=0,
                step=action_step,
                plugins=self.plugins,
                callback=simple_callback
            )
        )

        execution = Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )

        execution.setup_queue()

        self.assertListEqual(execution.queue, [])

    def test_instantiating_sequential_flow_callback(self):
        task = Task(
            task_id=5,
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback
        )

        group = QueueGroup()
        group.add(item=task)

        execution = Sequential(
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            group=group,
            plugins=self.plugins
        )

        execution.setup_queue()
        execution._flow_callback(task=task)

        tasks = execution.transport()
        self.assertEqual(tasks[0].task_id, 5)
