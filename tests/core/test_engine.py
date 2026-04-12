"""Test TaskEngine"""

import logging
import unittest
from uuid import uuid4

from pytest import fixture  # type: ignore

from dotflow.core.context import Context
from dotflow.core.engine import TaskEngine
from dotflow.core.task import Task
from dotflow.core.types import TypeStatus
from tests.mocks import (
    ActionStep,
    ActionStepExecutionOrderer,
    ActionStepWithContexts,
    ActionStepWithError,
    ActionStepWithInitialContext,
    ActionStepWithPreviousContext,
    SimpleStep,
    action_step,
    action_step_valid_object,
    action_step_with_contexts,
    action_step_with_error,
    action_step_with_initial_context,
    action_step_with_previous_context,
    action_step_with_retry,
    action_step_with_timeout,
    simple_callback,
    simple_step,
)


class TestTaskEngine(unittest.TestCase):
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setUp(self):
        self.workflow_id = uuid4()
        self.context = {"context": True}
        self.task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)

    def test_engine_with_function_completed(self):
        workflow_id = uuid4()
        task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)
        engine = TaskEngine(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.workflow_id, workflow_id)
        self.assertIsNotNone(task.duration)

    def test_engine_with_function_failed(self):
        workflow_id = uuid4()
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step_with_error, callback=simple_callback
        )
        engine = TaskEngine(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.FAILED)
        self.assertEqual(task.workflow_id, workflow_id)

    def test_engine_with_class_completed(self):
        execution_log = ""
        workflow_id = uuid4()
        task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=ActionStep, callback=simple_callback)
        engine = TaskEngine(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        with self._caplog.at_level(logging.NOTSET):
            with engine.start():
                engine.execute()

            for log in self._caplog.records:
                if log.funcName == "run":
                    execution_log = log.message

        self.assertEqual(execution_log, "ActionStep: Run function executed")
        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.workflow_id, workflow_id)

    def test_engine_with_class_failed(self):
        execution_log = ""
        workflow_id = uuid4()
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=ActionStepWithError, callback=simple_callback
        )
        engine = TaskEngine(
            task=task, workflow_id=workflow_id, previous_context=Context()
        )

        with self._caplog.at_level(logging.NOTSET):
            with engine.start():
                engine.execute()

            for log in self._caplog.records:
                if log.funcName == "run":
                    execution_log = log.message

        self.assertEqual(
            execution_log, "ActionStepWithError: Run function executed"
        )
        self.assertEqual(task.status, TypeStatus.FAILED)
        self.assertEqual(task.workflow_id, workflow_id)

    def test_engine_function_with_initial_context(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_initial_context,
            callback=simple_callback,
            initial_context=self.context,
        )
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=None
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.initial_context.storage, self.context)

    def test_engine_function_with_previous_context(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_previous_context,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context,
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task._previous_context.storage, self.context)

    def test_engine_function_with_contexts(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_contexts,
            callback=simple_callback,
            initial_context=self.context,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context,
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.initial_context.storage, self.context)
        self.assertEqual(task.previous_context.storage, self.context)

    def test_engine_class_with_initial_context(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=ActionStepWithInitialContext,
            callback=simple_callback,
            initial_context=self.context,
        )
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=None
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.initial_context.storage, self.context)

    def test_engine_class_with_previous_context(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=ActionStepWithPreviousContext,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context,
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.previous_context.storage, self.context)
        self.assertEqual(
            task.current_context.storage[0].storage, {"func": "run_x"}
        )
        self.assertEqual(
            task.current_context.storage[1].storage, {"func": "run_y"}
        )

    def test_engine_class_with_contexts(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=ActionStepWithContexts,
            callback=simple_callback,
            initial_context=self.context,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=self.context,
        )

        with engine.start():
            engine.execute()

        self.assertEqual(task.status, TypeStatus.COMPLETED)
        self.assertEqual(task.initial_context.storage, self.context)
        self.assertEqual(task.previous_context.storage, self.context)
        self.assertEqual(
            task.current_context.storage[0].storage, {"foo": "bar"}
        )

    def test_engine_is_action_true(self):
        engine = TaskEngine(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        with engine.start():
            engine.execute()

        class_instance = ActionStep(task=engine.task).storage
        self.assertTrue(
            engine._is_action(class_instance=class_instance, func="run")
        )

    def test_engine_is_action_false(self):
        engine = TaskEngine(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        with engine.start():
            engine.execute()

        class_instance = SimpleStep()
        self.assertFalse(
            engine._is_action(class_instance=class_instance, func="run")
        )

    def test_engine_is_action_init_false(self):
        engine = TaskEngine(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        with engine.start():
            engine.execute()

        class_instance = SimpleStep()
        self.assertFalse(
            engine._is_action(class_instance=class_instance, func="__init__")
        )

    def test_engine_execution_orderer(self):
        expected_value = [
            (3, "func_f"),
            (7, "func_e"),
            (11, "func_d"),
            (15, "func_c"),
            (19, "func_b"),
            (23, "func_a"),
        ]

        engine = TaskEngine(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        with engine.start():
            engine.execute()

        class_instance = ActionStepExecutionOrderer(task=engine.task).storage
        callable_list = [
            func
            for func in dir(class_instance)
            if engine._is_action(class_instance, func)
        ]

        self.assertListEqual(
            engine._execution_orderer(
                callable_list=callable_list, class_instance=class_instance
            ),
            expected_value,
        )

    def test_engine_valid_objects(self):
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
            memoryview(bytes(5)),
        ]

        for input_value in valid_objects:
            task = Task(
                task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
                step=action_step_valid_object,
                callback=simple_callback,
                initial_context=input_value,
            )

            engine = TaskEngine(
                task=task, workflow_id=self.workflow_id, previous_context=None
            )

            with engine.start():
                engine.execute()

            self.assertEqual(task.status, TypeStatus.COMPLETED)
            self.assertEqual(task.current_context.storage, input_value)

    def test_engine_status_in_progress_during_execution(self):
        captured_status = None

        task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )

        with engine.start():
            captured_status = task.status
            engine.execute()

        self.assertEqual(captured_status, TypeStatus.IN_PROGRESS)
        self.assertEqual(task.status, TypeStatus.COMPLETED)

    def test_engine_context_manager_without_execute(self):
        task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )

        with engine.start():
            pass

        self.assertEqual(task.status, TypeStatus.COMPLETED)

    def test_engine_execute_with_retry_completed(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_retry,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )

        with engine.start():
            engine.execute_with_retry()

        self.assertEqual(task.status, TypeStatus.COMPLETED)

    def test_engine_execute_with_retry_failed(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_error,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )

        with engine.start():
            engine.execute_with_retry()

        self.assertEqual(task.status, TypeStatus.FAILED)

    def test_engine_execute_with_timeout(self):
        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_timeout,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task, workflow_id=self.workflow_id, previous_context=Context()
        )

        with engine.start():
            engine.execute_with_retry()

        self.assertEqual(task.status, TypeStatus.COMPLETED)

    def test_timeout_expired_marks_task_failed(self):
        from time import sleep as _sleep

        from dotflow import action

        @action(timeout=1)
        def slow_step():
            _sleep(5)
            return {"done": True}

        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=slow_step,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        with engine.start():
            engine.execute_with_retry()

        self.assertEqual(task.status, TypeStatus.FAILED)

    def test_futures_timeout_error_converted_to_builtin(self):
        from concurrent.futures import (
            TimeoutError as FuturesTimeoutError,
        )
        from unittest.mock import MagicMock, patch

        task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            step=action_step_with_timeout,
            callback=simple_callback,
        )
        engine = TaskEngine(
            task=task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )

        mock_future = MagicMock()
        mock_future.result.side_effect = FuturesTimeoutError("timed out")

        with patch("dotflow.core.engine.ThreadPoolExecutor") as mock_pool:
            mock_pool.return_value.submit.return_value = mock_future

            with self.assertRaises(TimeoutError):
                engine._execute_with_timeout(seconds=1)
