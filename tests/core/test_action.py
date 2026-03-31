"""Test context of actions"""

import logging
import unittest

from pytest import fixture  # type: ignore

from dotflow.core.action import Action
from dotflow.core.context import Context
from dotflow.core.task import Task
from dotflow.core.types.status import TypeStatus
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
        self.task = Task(task_id=1, step=action_step)

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

    def test_instantiating_action_class_with_fail_retry(self):
        error_message = "Fail!"
        number_of_retries = 5

        inside = Action(simple_step_with_fail, retry=number_of_retries)

        with self._caplog.at_level(logging.ERROR):
            try:
                inside()
            except Exception as error:
                self.assertEqual(error.args[0], error_message)

            self.assertEqual(len(self._caplog.records), number_of_retries)

            for record in self._caplog.records:
                self.assertEqual(record.message, error_message)

    def test_sets_retry_status_before_retrying(self):
        calls = {"count": 0}
        statuses = []

        def flaky_step():
            calls["count"] += 1
            if calls["count"] == 1:
                raise Exception("Fail once")
            statuses.append(self.task.status)
            return "ok"

        inside = Action(flaky_step, retry=2, retry_delay=0)
        inside(task=self.task)

        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0], TypeStatus.RETRY)

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
