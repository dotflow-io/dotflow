"""Test context of utils"""

import unittest

from dotflow.core.utils import callback, simple


class TestUtils(unittest.TestCase):

    def test_callback(self):
        callback()

    def test_exec(self):
        simple()
