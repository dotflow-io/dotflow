"""Test context of actions"""

import logging
import unittest

from pytest import fixture  # type: ignore

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from tests.mocks import (
    action_step,
    simple_step,
    simple_step_with_fail,
    simple_step_with_initial_context,
    simple_step_with_params,
    simple_step_with_previous_context,
)


class TestClassActions(unittest.TestCase):
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog
        self.task = Task(
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step
        )

    def test_instantiating_action_class(self):
        number_of_retries = 1

        inside = Action(simple_step, task=self.task)
        decorated_function = inside(task=self.task)

        self.assertEqual(inside.retry, number_of_retries)
        self.assertEqual(inside.func, simple_step)
        self.assertIsInstance(decorated_function, Context)

    def test_instantiating_action_class_with_retry(self):
        number_of_retries = 5

        inside = Action(simple_step, task=self.task, retry=number_of_retries)
        decorated_function = inside(task=self.task)

        self.assertEqual(inside.retry, number_of_retries)
        self.assertEqual(inside.func, simple_step)
        self.assertIsInstance(decorated_function, Context)

    def test_instantiating_action_class_with_fail(self):
        error_message = "Fail!"

        inside = Action(simple_step_with_fail)

        with self.assertRaises(Exception) as ctx:
            inside()

        self.assertEqual(str(ctx.exception), error_message)

    def test_retry_zero_still_executes_task_once(self):
        call_count = {"n": 0}

        def counting_step():
            call_count["n"] += 1

        inside = Action(counting_step, retry=0)
        inside(task=self.task)

        self.assertEqual(
            call_count["n"],
            1,
            "retry=0 should execute the task exactly once, not zero times",
        )

    def test_retry_zero_raises_on_failure(self):
        def always_fail():
            raise ValueError("fail")

        inside = Action(always_fail, retry=0)
        with self.assertRaises(ValueError):
            inside(task=self.task)

    def test_action_single_attempt_raises_on_failure(self):
        def always_fail():
            raise ValueError("fail")

        inside = Action(always_fail)
        with self.assertRaises(ValueError):
            inside(task=self.task)

    def test_retry_exception_does_not_chain_to_itself(self):
        def always_fail():
            raise ValueError("fail")

        inside = Action(always_fail, retry=2, retry_delay=0)

        try:
            inside()
        except ValueError as error:
            self.assertIsNot(
                error.__cause__,
                error,
                "Exception must not be its own __cause__ (circular chain)",
            )

    def test_action_preserves_retry_params(self):
        inside = Action(simple_step, retry=3, retry_delay=2, backoff=True)

        self.assertEqual(inside.retry, 3)
        self.assertEqual(inside.retry_delay, 2)
        self.assertTrue(inside.backoff)

    def test_action_class_with_previous_context(self):
        inside = Action(simple_step_with_previous_context, task=self.task)

        with self._caplog.at_level(logging.DEBUG):
            inside(task=self.task)
            self.assertEqual(self._caplog.records[0].message, "None")

    def test_set_params_previous_context(self):
        inside = Action(simple_step_with_previous_context)
        inside._set_params()

        self.assertListEqual(inside.params, ["previous_context"])

    def test_set_params_initial_context(self):
        inside = Action(simple_step_with_initial_context)
        inside._set_params()

        self.assertListEqual(inside.params, ["initial_context"])

    def test_get_context_with_initial_context(self):
        input_value = {"initial_context": "bar"}

        inside = Action(simple_step_with_initial_context)
        inside.params = ["initial_context"]
        result = inside._get_context(kwargs=input_value)

        self.assertIsInstance(result["initial_context"], Context)
        self.assertEqual(result["initial_context"].storage, "bar")

    def test_get_context_with_previous_context(self):
        input_value = {"previous_context": "foo"}

        inside = Action(simple_step_with_previous_context)
        inside.params = ["previous_context"]
        result = inside._get_context(kwargs=input_value)

        self.assertIsInstance(result["previous_context"], Context)
        self.assertEqual(result["previous_context"].storage, "foo")

    def test_get_context_without_content(self):
        expected_value = {}

        inside = Action(simple_step)
        result = inside._get_context(kwargs=expected_value)

        self.assertEqual(result, expected_value)

    def test_get_context_without_context_params(self):
        mock_values = {"foo": True, "bar": True}

        inside = Action(simple_step_with_params)
        result = inside._get_context(kwargs=mock_values)

        self.assertEqual(result, {})
