"""Test context of actions"""

import unittest
import logging

from pytest import fixture  # type: ignore

from dotflow.core.context import Context
from dotflow.core.action import Action

from tests.mocks import (
    simple_step,
    simple_step_with_params,
    simple_step_with_initial_context,
    simple_step_with_previous_context,
    simple_step_with_fail
)


class TestClassActions(unittest.TestCase):

    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_instantiating_action_class(self):
        number_of_retries = 1

        inside = Action(simple_step)
        decorated_function = inside()

        self.assertEqual(inside.retry, number_of_retries)
        self.assertEqual(inside.func, simple_step)
        self.assertIsInstance(decorated_function, Context)

    def test_instantiating_action_class_with_retry(self):
        number_of_retries = 5

        inside = Action(simple_step, retry=number_of_retries)
        decorated_function = inside()

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

    def test_action_class_with_previous_context(self):
        inside = Action(simple_step_with_previous_context)

        with self._caplog.at_level(logging.DEBUG):
            inside()
            self.assertEqual(self._caplog.records[0].message, 'None')

    def test_set_params_previous_context(self):
        inside = Action(simple_step_with_previous_context)
        inside._set_params()

        self.assertListEqual(inside.params, ["previous_context"])

    def test_set_params_initial_context(self):
        inside = Action(simple_step_with_initial_context)
        inside._set_params()

        self.assertListEqual(inside.params, ["initial_context"])

    def test_get_context_with_initial_context(self):
        expected_value = {"initial_context": "bar"}

        inside = Action(simple_step_with_initial_context)
        inside.params = ["initial_context"]
        result = inside._get_context(kwargs=expected_value)

        self.assertEqual(result, expected_value)

    def test_get_context_with_previous_context(self):
        expected_value = {"previous_context": "foo"}

        inside = Action(simple_step_with_previous_context)
        inside.params = ["previous_context"]
        result = inside._get_context(kwargs=expected_value)

        self.assertEqual(result, expected_value)

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
