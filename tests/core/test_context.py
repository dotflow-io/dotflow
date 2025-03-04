"""Test context of context"""

import unittest

from datetime import datetime
from dotflow.core.context import Context


class TestContext(unittest.TestCase):

    def setUp(self):
        self.content = {"foo": "bar"}

    def test_instantiating_context_class(self):
        context = Context(storage=self.content)

        self.assertIsInstance(context.time, datetime)
        self.assertEqual(context.storage, self.content)

    def test_instantiates_context_with_context(self):
        context = Context(
            storage=Context(storage=self.content)
        )

        self.assertIsInstance(context.time, datetime)
        self.assertEqual(context.storage, self.content)
