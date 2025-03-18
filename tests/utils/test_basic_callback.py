"""Test utils"""

import unittest

from dotflow.utils import basic_callback


class TestBasicCallback(unittest.TestCase):

    def test_callback(self):
        basic_callback()
