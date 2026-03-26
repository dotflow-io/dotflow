"""Tests to ensure queue.get() does not deadlock when a task fails early."""

import unittest

from uuid import uuid4

from dotflow.core.workflow import Parallel, SequentialGroup, grouper
from dotflow.core.types import TypeStatus
from dotflow.core.task import Task

from tests.mocks import action_step, action_step_with_error, simple_callback


class TestWorkflowParallelDeadlock(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()

    def test_parallel_does_not_deadlock_on_failed_task(self):
        """get_tasks() must return even when a task fails (never puts to queue)."""
        tasks = [Task(task_id=0, step=action_step_with_error, callback=simple_callback)]

        execution = Parallel(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=False,
            groups=grouper(tasks=tasks),
        )

        result = execution.get_tasks()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status, TypeStatus.FAILED)

    def test_parallel_processes_attribute_initialized(self):
        """_processes must be initialized in setup_queue."""
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        execution = Parallel(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=False,
            groups=grouper(tasks=tasks),
        )
        execution.setup_queue()

        self.assertIsInstance(execution._processes, list)


class TestWorkflowSequentialGroupDeadlock(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()

    def test_sequential_group_does_not_deadlock_on_failed_task(self):
        """get_tasks() must return even when a group task fails early."""
        tasks = [Task(task_id=0, step=action_step_with_error, callback=simple_callback)]

        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=False,
            groups=grouper(tasks=tasks),
        )

        result = execution.get_tasks()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status, TypeStatus.FAILED)

    def test_sequential_group_processes_attribute_initialized(self):
        """_processes must be initialized in setup_queue."""
        tasks = [Task(task_id=0, step=action_step, callback=simple_callback)]
        execution = SequentialGroup(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=False,
            groups=grouper(tasks=tasks),
        )
        execution.setup_queue()

        self.assertIsInstance(execution._processes, list)
