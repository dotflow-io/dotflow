"""Test context of actions"""

import unittest
import logging

from pytest import fixture

from dotflow.core.context import Context
from dotflow.core.action import Action

from tests.mocks import (
    simple_step,
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

    def test_has_context_true(self):
        inside = Action(simple_step_with_previous_context)

        self.assertTrue(inside._has_context())

    def test_has_context_false(self):
        inside = Action(simple_step)

        self.assertFalse(inside._has_context())

    def test_get_context_with_content(self):
        inside = Action(simple_step)
        result = inside._get_context(kwargs={"previous_context": "foo"})

        self.assertEqual(result, "foo")

    def test_get_context_without_content(self):
        inside = Action(simple_step)
        result = inside._get_context(kwargs={})

        self.assertIsInstance(result, Context)
