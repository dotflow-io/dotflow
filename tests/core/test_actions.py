"""Test context of actions"""

import unittest
import logging

from pytest import fixture

from dotflow.core.context import Context
from dotflow.core.actions import action


def dummy_step():
    pass


def dummy_step_previous_context(previous_context):
    logging.debug(previous_context.storage)


class TestActions(unittest.TestCase):

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
            assert self._caplog.records[0].message == 'None'
