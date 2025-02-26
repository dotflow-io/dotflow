"""Test context of utils"""

import unittest

from dotflow.core.utils import callback, exec


class TestUtils(unittest.TestCase):

    def test_callback(self):
        callback()

    def test_exec(self):
        exec()
