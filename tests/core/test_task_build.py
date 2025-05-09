"""Test context of task build"""

import unittest
from uuid import uuid4

from dotflow.core.config import Config
from dotflow.core.context import Context
from dotflow.core.exception import MissingActionDecorator
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.serializers.workflow import SerializerWorkflow
from dotflow.core.serializers.task import SerializerTask
from dotflow.utils import basic_callback

from tests.mocks import action_step, simple_step, SimpleStep


class TestTaskBuild(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.content = {"foo": "bar"}

    def test_instantiating_task_build_class(self):
        task = TaskBuilder(config=self.config)

        self.assertListEqual(task.queue, [])

    def test_add_method(self):
        task = TaskBuilder(config=self.config)
        task.add(step=action_step)

        self.assertEqual(task.queue[0].task_id, 0)
        self.assertIsInstance(task.queue[0], Task)
        self.assertEqual(task.queue[0].callback, basic_callback)
        self.assertEqual(len(task.queue), 1)

    def test_add_method_with_class_context(self):
        task = TaskBuilder(config=self.config)
        task.add(step=action_step, initial_context=Context(storage=self.content))

        self.assertEqual(task.queue[0].initial_context.storage, self.content)

        self.assertIsInstance(task.queue[0].initial_context, Context)

    def test_add_method_without_class_context(self):
        task = TaskBuilder(config=self.config)
        task.add(step=action_step, initial_context=self.content)

        self.assertEqual(task.queue[0].initial_context.storage, self.content)

        self.assertIsInstance(task.queue[0].initial_context, Context)

    def test_count_method(self):
        task = TaskBuilder(config=self.config)

        initial_count = 0
        final_count = 1

        self.assertEqual(task.count(), initial_count)

        task.add(step=action_step)

        self.assertEqual(task.count(), final_count)

    def test_clear_method(self):
        task = TaskBuilder(config=self.config)

        expected_count_before = 1
        expected_count_after = 0

        task.add(step=action_step)
        self.assertEqual(task.count(), expected_count_before)

        task.clear()

        self.assertEqual(task.count(), expected_count_after)

    def test_with_method_step_without_decorator(self):
        task = TaskBuilder(config=self.config)

        with self.assertRaises(MissingActionDecorator):
            task.add(step=simple_step)

    def test_with_class_step_without_decorator(self):
        task = TaskBuilder(config=self.config)

        with self.assertRaises(MissingActionDecorator):
            task.add(step=SimpleStep)

    def test_task_build_schema(self):
        expected_workflow_id = uuid4()

        task = TaskBuilder(config=self.config, workflow_id=expected_workflow_id)
        task.add(step=action_step, initial_context=self.content)

        schema = task.schema()

        self.assertIsInstance(schema, SerializerWorkflow)
        self.assertIsInstance(schema.tasks[0], SerializerTask)

    def test_task_build_result(self):
        expected_workflow_id = uuid4()
        expected_result = {
            "workflow_id": str(expected_workflow_id),
            "tasks": [
                {
                    "task_id": 0,
                    "workflow_id": str(expected_workflow_id),
                    "status": "Not started",
                    "error": None,
                    "duration": None,
                    "initial_context": '{"foo": "bar"}',
                    "current_context": None,
                    "previous_context": None,
                    "group_name": "default",
                }
            ],
        }

        task = TaskBuilder(config=self.config, workflow_id=expected_workflow_id)
        task.add(step=action_step, initial_context=self.content)

        result = task.result()
        self.assertEqual(result, expected_result)
