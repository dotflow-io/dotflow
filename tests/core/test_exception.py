"""Test context of exception"""


import unittest

from dotflow.core.exception import (
    MissingActionDecorator,
    ExecutionModeNotExist,
    StepMissingInit,
    MESSAGE_MISSING_STEP_DECORATOR,
    MESSAGE_EXECUTION_NOT_EXIST,
    MESSAGE_STEP_MISSING_INIT
)


class TestException(unittest.TestCase):

    def test_missing_action_decorator(self):
        exception = MissingActionDecorator()

        self.assertEqual(
            exception.args[0],
            MESSAGE_MISSING_STEP_DECORATOR
        )

    def test_execution_mode_not_exist(self):
        exception = ExecutionModeNotExist()

        self.assertEqual(
            exception.args[0],
            MESSAGE_EXECUTION_NOT_EXIST
        )

    def test_step_missing_init(self):
        exception = StepMissingInit(name="Step")

        self.assertEqual(
            exception.args[0],
            MESSAGE_STEP_MISSING_INIT.format(name="Step")
        )
