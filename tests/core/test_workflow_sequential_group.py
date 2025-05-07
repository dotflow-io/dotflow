"""Test context of controller"""

import unittest

from uuid import uuid4

from multiprocessing.queues import Queue

from dotflow.core.workflow import SequentialGroup, grouper
from dotflow.core.types import TypeStatus
from dotflow.core.task import Task, TaskError

from tests.mocks import (
    action_step,
    action_step_with_error,
    simple_callback,
)


class TestWorkflowSequentialGroup(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()
        self.ignore = False

    def test_instantiating_sequential_group_class(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        tasks = execution.get_tasks()

        self.assertListEqual(tasks, tasks)
        self.assertDictEqual(execution.groups, groups)
        self.assertEqual(execution.workflow_id, self.workflow_id)
        self.assertEqual(execution.ignore, self.ignore)

    def test_workflow_with_sequential_group_function_completed(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]

        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        tasks = execution.get_tasks()

        self.assertEqual(tasks[0].status, TypeStatus.COMPLETED)
        self.assertEqual(tasks[0].current_context.storage, {"foo": "bar"})
        self.assertIsInstance(tasks[0].error, TaskError)
        self.assertEqual(tasks[0].error.message, "")

    def test_workflow_with_sequential_group_function_failed(self):
        tasks = [Task(task_id=0, step=action_step_with_error, callback=simple_callback)]

        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        tasks = execution.get_tasks()

        self.assertEqual(tasks[0].status, TypeStatus.FAILED)
        self.assertIsNone(tasks[0].current_context.storage)
        self.assertIsInstance(tasks[0].error, TaskError)
        self.assertEqual(tasks[0].error.message, "Fail!")

    def test_instantiating_sequential_group_setup_queue(self):
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()

        self.assertIsInstance(execution.queue, Queue)

    def test_instantiating_sequential_group_flow_callback(self):
        task = Task(task_id=5, step=action_step, callback=simple_callback)
        groups = grouper(tasks=[task])

        execution = SequentialGroup(
            tasks=[task],
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()
        execution._flow_callback(task=task)

        tasks = execution.get_tasks()
        self.assertEqual(tasks[0].task_id, 5)
