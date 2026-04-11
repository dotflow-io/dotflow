"""Test context of context"""

import unittest
from datetime import datetime
from uuid import uuid4

from dotflow.core.context import Context


class TestContext(unittest.TestCase):
    def setUp(self):
        self.content = {"foo": "bar"}

    def test_instantiating_context_class(self):
        context = Context(storage=self.content)

        self.assertIsInstance(context.time, datetime)
        self.assertEqual(context.storage, self.content)

    def test_instantiates_context_with_context(self):
        context = Context(storage=Context(storage=self.content))

        self.assertIsInstance(context.time, datetime)
        self.assertEqual(context.storage, self.content)


class TestContextTaskIdSetter(unittest.TestCase):
    def test_valid_int(self):
        ctx = Context(task_id=5)
        self.assertEqual(ctx.task_id, 5)

    def test_none_is_allowed(self):
        ctx = Context()
        ctx.task_id = None
        self.assertIsNone(ctx.task_id)

    def test_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            Context(task_id="5")

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            Context(task_id=3.14)

    def test_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            Context(task_id=[1])


class TestContextWorkflowIdSetter(unittest.TestCase):
    def test_valid_uuid(self):
        uid = uuid4()
        ctx = Context(workflow_id=uid)
        self.assertEqual(ctx.workflow_id, uid)

    def test_valid_uuid_string(self):
        uid = uuid4()
        ctx = Context(workflow_id=str(uid))
        self.assertEqual(ctx.workflow_id, uid)

    def test_none_is_allowed(self):
        ctx = Context()
        ctx.workflow_id = None
        self.assertIsNone(ctx.workflow_id)

    def test_invalid_uuid_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            Context(workflow_id="not-a-uuid")

    def test_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            Context(workflow_id=12345)

    def test_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            Context(workflow_id=[1, 2, 3])
