"""Test context of execution"""

import logging
import unittest

from pytest import fixture  # type: ignore

from uuid import uuid4

from dotflow.core.context import Context
from dotflow.core.execution import Execution
from dotflow.core.types import TypeStatus
from dotflow.core.task import Task

from tests.mocks import (
    ActionStep,
    ActionStepWithInitialContext,
    ActionStepWithPreviousContext,
    ActionStepWithContexts,
    ActionStepWithError,
    SimpleStep,
    ActionStepExecutionOrderer,
    action_step,
    action_step_valid_object,
    action_step_with_initial_context,
    action_step_with_previous_context,
    action_step_with_contexts,
    action_step_with_error,
    simple_callback,
    simple_step,
)


class TestExecution(unittest.TestCase):

    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.workflow_id = uuid4()
        self.context = {"context": True}
        self.task = Task(task_id=0, step=action_step, callback=simple_callback)

    def test_execution_with_function_completed(self):
        workflow_id = uuid4()
        task = Task(task_id=0, step=action_step, callback=simple_callback)
        controller = Execution(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_function_failed(self):
        workflow_id = uuid4()
        task = Task(task_id=0, step=action_step_with_error, callback=simple_callback)
        controller = Execution(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        self.assertEqual(controller.task.status, TypeStatus.FAILED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_class_completed(self):
        execution_log = ""
        workflow_id = uuid4()

        task = Task(task_id=0, step=ActionStep, callback=simple_callback)

        with self._caplog.at_level(logging.NOTSET):
            controller = Execution(
                task=task, workflow_id=workflow_id, previous_context=Context()
            )

            for log in self._caplog.records:
                if log.funcName == "run":
                    execution_log = log.message

        self.assertEqual(execution_log, "ActionStep: Run function executed")
        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_with_class_failed(self):
        execution_log = ""
        workflow_id = uuid4()

        task = Task(task_id=0, step=ActionStepWithError, callback=simple_callback)

        with self._caplog.at_level(logging.NOTSET):
            controller = Execution(
                task=task, workflow_id=workflow_id, previous_context=Context()
            )

            for log in self._caplog.records:
                if log.funcName == "run":
                    execution_log = log.message

        self.assertEqual(execution_log, "ActionStepWithError: Run function executed")
        self.assertEqual(controller.task.status, TypeStatus.FAILED)
        self.assertEqual(controller.task.workflow_id, workflow_id)

    def test_execution_function_with_initial_context(self):
        task = Task(
            task_id=0,
            step=action_step_with_initial_context,
            callback=simple_callback,
            initial_context=self.context,
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=None
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)

    def test_execution_function_with_previous_context(self):
        task = Task(
            task_id=0, step=action_step_with_previous_context, callback=simple_callback
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=self.context
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task._previous_context.storage, self.context)

    def test_execution_function_with_contexts(self):
        task = Task(
            task_id=0,
            step=action_step_with_contexts,
            callback=simple_callback,
            initial_context=self.context,
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=self.context
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)
        self.assertEqual(controller.task.previous_context.storage, self.context)

    def test_execution_class_with_initial_context(self):
        task = Task(
            task_id=0,
            step=ActionStepWithInitialContext,
            callback=simple_callback,
            initial_context=self.context,
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=None
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)

    def test_execution_class_with_previous_context(self):
        task = Task(
            task_id=0, step=ActionStepWithPreviousContext, callback=simple_callback
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=self.context
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.previous_context.storage, self.context)

        self.assertEqual(
            controller.task.current_context.storage[0].storage, {"func": "run_x"}
        )
        self.assertEqual(
            controller.task.current_context.storage[1].storage, {"func": "run_y"}
        )

    def test_execution_class_with_contexts(self):
        task = Task(
            task_id=0,
            step=ActionStepWithContexts,
            callback=simple_callback,
            initial_context=self.context,
        )
        controller = Execution(
            task=task, workflow_id=self.workflow_id, previous_context=self.context
        )

        self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
        self.assertEqual(controller.task.initial_context.storage, self.context)
        self.assertEqual(controller.task.previous_context.storage, self.context)

        self.assertEqual(controller.task.initial_context.storage, {"context": True})
        self.assertEqual(controller.task.previous_context.storage, {"context": True})
        self.assertEqual(
            controller.task.current_context.storage[0].storage, {"foo": "bar"}
        )

    def test_is_action_true(self):
        controller = Execution(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context()
        )

        class_instance = ActionStep(task=controller.task).storage
        self.assertTrue(
            controller._is_action(class_instance=class_instance, func="run")
        )

    def test_is_action_false(self):
        controller = Execution(
            task=self.task, workflow_id=self.workflow_id, previous_context=Context()
        )

        class_instance = SimpleStep()
        self.assertFalse(
            controller._is_action(class_instance=class_instance, func="run")
        )

    def test_is_action_init_false(self):
        controller = Execution(
            task=self.task, workflow_id=self.workflow_id, previous_context=Context()
        )

        class_instance = SimpleStep()
        self.assertFalse(
            controller._is_action(class_instance=class_instance, func="__init__")
        )

    def test_execution_orderer(self):
        expected_value = [
            (4, "func_f"),
            (8, "func_e"),
            (12, "func_d"),
            (16, "func_c"),
            (20, "func_b"),
            (24, "func_a"),
        ]

        controller = Execution(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context()
        )

        class_instance = ActionStepExecutionOrderer(task=controller.task).storage
        callable_list = [
            func
            for func in dir(class_instance)
            if controller._is_action(class_instance, func)
        ]

        self.assertListEqual(
            controller._execution_orderer(
                callable_list=callable_list, class_instance=class_instance
            ),
            expected_value,
        )

    def test_valid_objects(self):
        valid_objects = [
            "",
            1,
            1.0,
            complex(3, 5),
            {},
            [],
            (1, 2, 3),
            {1, 2, 3},
            frozenset({1, 2, 3}),
            range(5),
            simple_step,
            True,
            None,
            b"Hello",
            bytearray(5),
            memoryview(bytes(5))
        ]

        for input_value in valid_objects:
            task = Task(
                task_id=0,
                step=action_step_valid_object,
                callback=simple_callback,
                initial_context=input_value,
            )

            controller = Execution(
                task=task,
                workflow_id=self.workflow_id,
                previous_context=None
            )

            self.assertEqual(controller.task.status, TypeStatus.COMPLETED)
            self.assertEqual(controller.task.current_context.storage, input_value)
