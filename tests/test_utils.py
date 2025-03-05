"""Test context of utils"""

import unittest

from dotflow.utils import basic_callback, basic_function


class TestUtils(unittest.TestCase):

    def test_callback(self):
        basic_callback()

    def test_function(self):
        basic_function()
