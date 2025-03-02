"""Test context of action"""

import unittest
import logging

from pytest import fixture

from dotflow.core.context import Context
from dotflow.core.decorators.action import action


from tests.mocks import (
    simple_step,
    simple_step_with_previous_context
)


class TestMethodAction(unittest.TestCase):

    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def test_instantiating_action_method(self):
        inside = action(simple_step)
        decorated_function = inside()

        self.assertIsInstance(decorated_function, Context)

    def test_action_with_previous_context(self):
        inside = action(simple_step_with_previous_context)

        with self._caplog.at_level(logging.DEBUG):
            inside()
            self.assertEqual(self._caplog.records[0].message, 'None')
