import unittest

from datetime import datetime
from dotflow.core.context import Context


class TestContext(unittest.TestCase):

    def setUp(self):
        self.example = {"foo": "bar"}

    def test_instantiating_class(self):
        context = Context(storage=self.example)

        self.assertIsInstance(context.datetime, datetime)
        self.assertEqual(context.storage, self.example)
