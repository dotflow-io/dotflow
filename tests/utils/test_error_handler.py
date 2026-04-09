"""Test error handler"""

import unittest

from dotflow.utils.error_handler import message_error, traceback_error


class TestTracebackError(unittest.TestCase):
    def test_returns_traceback_from_error_parameter(self):
        try:
            1 / 0
        except ZeroDivisionError as e:
            saved_error = e

        result = traceback_error(saved_error)

        self.assertIn("ZeroDivisionError", result)
        self.assertIn("division by zero", result)

    def test_works_outside_except_block(self):
        try:
            raise ValueError("test error")
        except ValueError as e:
            saved_error = e

        result = traceback_error(saved_error)

        self.assertIn("ValueError", result)
        self.assertIn("test error", result)

    def test_includes_traceback_lines(self):
        try:
            raise RuntimeError("boom")
        except RuntimeError as e:
            saved_error = e

        result = traceback_error(saved_error)

        self.assertIn("Traceback", result)
        self.assertIn("RuntimeError: boom", result)


class TestMessageError(unittest.TestCase):
    def test_returns_error_message(self):
        error = ValueError("something went wrong")

        result = message_error(error)

        self.assertEqual(result, "something went wrong")
