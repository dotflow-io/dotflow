"""Test context of controller"""

import unittest
from multiprocessing import get_context
from uuid import uuid4

from dotflow.core.task import Task, TaskError
from dotflow.core.types import TypeStatus
from dotflow.core.workflow import Parallel, grouper
from tests.mocks import (
    action_step,
    action_step_with_error,
    simple_callback,
)

Queue = type(get_context("fork").Queue())


class TestWorkflowParallel(unittest.TestCase):
    def setUp(self):
        self.workflow_id = uuid4()
        self.ignore = False

    def test_instantiating_parallel_class(self):
        tasks = [Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = Parallel(
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

    def test_workflow_with_parallel_function_completed(self):
        tasks = [Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)]

        execution = Parallel(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        tasks = execution.get_tasks()

        self.assertEqual(tasks[0].status, TypeStatus.COMPLETED)
        self.assertEqual(tasks[0].current_context.storage, {"foo": "bar"})
        self.assertEqual(tasks[0].errors, [])

    def test_workflow_with_parallel_function_failed(self):
        tasks = [
            Task(
                task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
                step=action_step_with_error,
                callback=simple_callback,
            )
        ]

        execution = Parallel(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=grouper(tasks=tasks),
        )

        tasks = execution.get_tasks()

        self.assertEqual(tasks[0].status, TypeStatus.FAILED)
        self.assertIsNone(tasks[0].current_context.storage)
        self.assertIsInstance(tasks[0].errors[-1], TaskError)
        self.assertEqual(tasks[0].errors[-1].message, "Fail!")

    def test_instantiating_parallel_setup_queue(self):
        tasks = [Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)]
        groups = grouper(tasks=tasks)

        execution = Parallel(
            tasks=tasks,
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()

        self.assertIsInstance(execution.queue, Queue)

    def test_instantiating_parallel_flow_callback(self):
        task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)
        groups = grouper(tasks=[task])

        execution = Parallel(
            tasks=[task],
            workflow_id=self.workflow_id,
            ignore=self.ignore,
            groups=groups,
        )

        execution.setup_queue()
        execution._flow_callback(task=task)

        tasks = execution.get_tasks()
        self.assertEqual(tasks[0].task_id, "01ARZ3NDEKTSV4RRFFQ69G5FAV")
