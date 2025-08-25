"""Test context of task"""

import json

import unittest
from uuid import uuid4

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.types.task import StatusTaskType
from dotflow.core.serializers.task import SerializerTaskError, SerializerTask
from dotflow.core.exception import (
    MissingActionDecorator,
    NotCallableObject,
    ImportModuleError,
)
from dotflow.core.task import Task, TaskError, TASK_GROUP_NAME
from dotflow.core.plugin import Plugin

from tests.mocks import action_step, simple_callback, simple_step


class TestTask(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()
        self.plugins = Plugin()
        self.task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback
        )
        self.content = {"foo": "bar"}

    def test_instantiating_task_class(self):
        task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            initial_context=Context(storage=self.content),
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback,
        )

        self.assertIsInstance(task.initial_context, Context)
        self.assertIsInstance(task.current_context, Context)
        self.assertIsInstance(task.previous_context, Context)
        self.assertIsInstance(task.error, TaskError)
        self.assertEqual(task.group_name, TASK_GROUP_NAME)

    def test_task_id(self):
        task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            initial_context=Context(storage=self.content),
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback,
        )

        self.assertEqual(task.task_id, 0)

    def test_workflow_id(self):
        workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=workflow_id,
            initial_context=Context(storage=self.content),
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback,
        )

        self.assertEqual(task.workflow_id, workflow_id)

    def test_task_schema(self):
        expected_error_message = "System error"
        expected_duration = 1.0
        expected_workflow_id = uuid4()

        task = Task(
            task_id=0,
            workflow_id=expected_workflow_id,
            initial_context=Context(storage=self.content),
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback,
        )

        try:
            raise SystemError(expected_error_message)
        except Exception as error:
            task.error = error

        task.current_context = self.content
        task.previous_context = self.content
        task.duration = expected_duration

        schema = task.schema()

        self.assertIsInstance(schema, SerializerTask)
        self.assertIsInstance(schema.error, SerializerTaskError)

        self.assertEqual(schema.task_id, 0)
        self.assertEqual(schema.workflow_id, expected_workflow_id)
        self.assertEqual(schema.status, StatusTaskType.IN_QUEUE)
        self.assertEqual(schema.error.message, expected_error_message)
        self.assertEqual(schema.duration, expected_duration)
        self.assertEqual(schema.initial_context, json.dumps(self.content))
        self.assertEqual(schema.current_context, json.dumps(self.content))
        self.assertEqual(schema.previous_context, json.dumps(self.content))
        self.assertEqual(schema.group_name, TASK_GROUP_NAME)

    def test_task_result(self):
        expected_duration = 1.0
        expected_workflow_id = uuid4()
        expected_result = {
            "task_id": 0,
            "workflow_id": str(expected_workflow_id),
            "status": "In queue",
            "error": {"traceback": "", "message": ""},
            "duration": expected_duration,
            "initial_context": '{"foo": "bar"}',
            "current_context": '{"foo": "bar"}',
            "previous_context": '{"foo": "bar"}',
            "group_name": TASK_GROUP_NAME,
        }
        task = Task(
            task_id=0,
            workflow_id=expected_workflow_id,
            initial_context=Context(storage=self.content),
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback,
        )

        task.current_context = self.content
        task.previous_context = self.content
        task.duration = expected_duration

        result = task.result()
        self.assertEqual(result, expected_result)


class TestTaskSetter(unittest.TestCase):

    def setUp(self):
        self.workflow_id = uuid4()
        self.plugins = Plugin()
        self.task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            step=action_step,
            plugins=self.plugins,
            callback=simple_callback
        )
        self.content = {"foo": "bar"}

    def test_set_step_with_path_module_success(self):
        input_value = "tests.mocks.step_function.action_step"
        expected_value = Action

        task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            step=input_value,
            plugins=self.plugins,
            callback=simple_callback
        )

        self.assertIsInstance(task.step, expected_value)

    def test_set_step_with_path_module_fail(self):
        input_value = "tests.mocks.step_function.XPTO"

        with self.assertRaises(ImportModuleError):
            Task(
                task_id=0,
                workflow_id=self.workflow_id,
                step=input_value,
                plugins=self.plugins,
                callback=simple_callback
            )

    def test_set_step_with_function_success(self):
        input_value = action_step
        expected_value = Action

        task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            step=input_value,
            plugins=self.plugins,
            callback=simple_callback
        )

        self.assertIsInstance(task.step, expected_value)

    def test_set_step_with_function_fail(self):
        input_value = simple_step

        with self.assertRaises(MissingActionDecorator):
            Task(
                task_id=0,
                workflow_id=self.workflow_id,
                step=input_value,
                plugins=self.plugins,
                callback=simple_callback
            )

    def test_set_callback_with_path_module_success(self):
        input_value = "tests.mocks.step_function.action_step"
        expected_value = Action

        task = Task(
            task_id=0,
            workflow_id=self.workflow_id,
            step=action_step,
            plugins=self.plugins,
            callback=input_value
        )

        self.assertIsInstance(task.step, expected_value)

    def test_set_callback_with_path_module_fail(self):
        input_value = "tests.mocks.step_function.XPTO"

        with self.assertRaises(ImportModuleError):
            Task(
                task_id=0,
                workflow_id=self.workflow_id,
                step=action_step,
                plugins=self.plugins,
                callback=input_value
            )

    def test_set_callback_with_path_module_not_callable_fail(self):
        input_value = "tests.mocks.constants.NOT_CALLABLE"

        with self.assertRaises(NotCallableObject):
            Task(
                task_id=0,
                workflow_id=self.workflow_id,
                step=action_step,
                plugins=self.plugins,
                callback=input_value
            )

    def test_set_initial_context(self):
        expected_value = Context(storage=self.content)

        self.task.initial_context = expected_value
        self.assertEqual(self.task.initial_context.storage, expected_value.storage)

    def test_set_previous_context(self):
        expected_value = Context(storage=self.content)

        self.task.previous_context = expected_value
        self.assertEqual(self.task.previous_context.storage, expected_value.storage)

    def test_set_current_context(self):
        expected_value = Context(storage=self.content)

        self.task.current_context = expected_value
        self.assertEqual(self.task.current_context.storage, expected_value.storage)

    def test_set_duration(self):
        expected_value = 42

        self.task.duration = expected_value
        self.assertEqual(self.task.duration, expected_value)

    def test_set_error(self):
        expected_value = "Fail!"

        try:
            raise Exception(expected_value)
        except Exception as err:
            self.task.error = err

        self.assertEqual(self.task.error.message, expected_value)
        self.assertIsInstance(self.task.error.exception, Exception)

    def test_set_status(self):
        expected_value = StatusTaskType.SUCCESS

        self.task.status = expected_value
        self.assertEqual(self.task.status, expected_value)
