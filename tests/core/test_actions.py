import unittest
import logging

from pytest import fixture

from dotflow.core.context import Context
from dotflow.core.actions import Action, action


def dummy_step():
    pass


def dummy_step_with_fail():
    logging.error("Fail!")
    raise Exception("Fail!")


def dummy_step_previous_context(previous_context):
    logging.debug(previous_context.storage)


class TestMethodActions(unittest.TestCase):

    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_instantiating_action_method(self):
        inside = action(dummy_step)
        decorated_function = inside()

        self.assertIsInstance(decorated_function, Context)

    def test_action_with_previous_context(self):
        inside = action(dummy_step_previous_context)

        with self._caplog.at_level(logging.DEBUG):
            inside()
            self.assertEqual(self._caplog.records[0].message, 'None')


class TestClassActions(unittest.TestCase):

    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_instantiating_action_class(self):
        number_of_retries = 1

        inside = Action(dummy_step)
        decorated_function = inside()

        self.assertEqual(inside._retry, number_of_retries)
        self.assertEqual(inside._func, dummy_step)
        self.assertIsInstance(decorated_function, Context)

    def test_instantiating_action_class_with_retry(self):
        number_of_retries = 5

        inside = Action(dummy_step, retry=number_of_retries)
        decorated_function = inside()

        self.assertEqual(inside._retry, number_of_retries)
        self.assertEqual(inside._func, dummy_step)
        self.assertIsInstance(decorated_function, Context)

    def test_instantiating_action_class_with_fail_retry(self):
        error_message = "Fail!"
        number_of_retries = 5

        inside = Action(dummy_step_with_fail, retry=number_of_retries)

        with self._caplog.at_level(logging.ERROR):
            try:
                inside()
            except Exception as error:
                self.assertEqual(error.args[0], error_message)

            self.assertEqual(len(self._caplog.records), number_of_retries)

            for record in self._caplog.records:
                self.assertEqual(record.message, error_message)
                
    def test_action_class_with_previous_context(self):
        inside = Action(dummy_step_previous_context)

        with self._caplog.at_level(logging.DEBUG):
            inside()
            self.assertEqual(self._caplog.records[0].message, 'None')
