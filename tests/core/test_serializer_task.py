"""Test SerializerTask model_dump_json"""

import json
import unittest

from dotflow.core.context import Context
from dotflow.core.serializers.task import SerializerTask


class TestSerializerTaskDumpJson(unittest.TestCase):
    def _make_task(self, **kwargs):
        defaults = {
            "task_id": 0,
            "_status": "Completed",
            "_duration": 1.5,
            "_initial_context": None,
            "_current_context": None,
            "_previous_context": None,
            "group_name": "default",
            "retry_count": 0,
            "_errors": [],
        }
        defaults.update(kwargs)
        return SerializerTask(**defaults)

    def test_returns_valid_json(self):
        task = self._make_task()
        result = task.model_dump_json()

        parsed = json.loads(result)
        self.assertEqual(parsed["task_id"], 0)
        self.assertEqual(parsed["status"], "Completed")

    def test_with_max_does_not_mutate_self(self):
        ctx = Context(storage={"large": "x" * 500})
        task = self._make_task(_initial_context=ctx, max=100)

        task.model_dump_json()
        task.model_dump_json()

        self.assertNotEqual(task.initial_context, task.size_message)

    def test_with_max_returns_valid_json(self):
        ctx = Context(storage={"large": "x" * 500})
        task = self._make_task(_initial_context=ctx, max=100)

        result = task.model_dump_json()
        json.loads(result)

    def test_with_max_replaces_contexts(self):
        task = self._make_task(
            _initial_context=Context(storage={"large": "x" * 500}),
            _current_context=Context(storage={"large": "y" * 500}),
            _previous_context=Context(storage={"large": "z" * 500}),
            max=200,
        )

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertEqual(parsed["initial_context"], "Context size exceeded")
        self.assertEqual(parsed["current_context"], "Context size exceeded")
        self.assertEqual(parsed["previous_context"], "Context size exceeded")

    def test_with_max_clears_errors_if_still_over(self):
        large_errors = [
            {
                "attempt": i,
                "exception": "Error",
                "traceback": "x" * 500,
                "message": "fail",
            }
            for i in range(10)
        ]
        task = self._make_task(_errors=large_errors, max=200)

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertEqual(parsed["errors"], [])
        self.assertIsNone(parsed["error"])

    def test_without_max_returns_full_json(self):
        ctx = Context(storage={"large": "x" * 500})
        task = self._make_task(_initial_context=ctx)

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertIn("large", str(parsed["initial_context"]))

    def test_none_context_returns_none(self):
        task = self._make_task(_current_context=None)

        parsed = json.loads(task.model_dump_json())
        self.assertIsNone(parsed["current_context"])

    def test_context_with_none_storage_returns_none(self):
        task = self._make_task(_current_context=Context(storage=None))

        parsed = json.loads(task.model_dump_json())
        self.assertIsNone(parsed["current_context"])

    def test_list_of_dicts(self):
        ctx = Context(storage=[{"id": 1}, {"id": 2}])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(len(parsed["current_context"]), 2)

    def test_list_of_strings(self):
        ctx = Context(storage=["hello", "world"])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(len(parsed["current_context"]), 2)

    def test_list_of_context_objects(self):
        inner_a = Context(storage={"name": "a"}, task_id=1)
        inner_b = Context(storage={"name": "b"}, task_id=2)
        ctx = Context(storage=[inner_a, inner_b])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("1", parsed["current_context"])
        self.assertIn("2", parsed["current_context"])

    def test_list_mixed_context_and_raw(self):
        inner = Context(storage={"nested": True}, task_id=5)
        ctx = Context(storage=[inner, {"raw": True}])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("5", parsed["current_context"])
        self.assertIn("1", parsed["current_context"])

    def test_list_context_without_task_id(self):
        inner = Context(storage={"data": True})
        ctx = Context(storage=[inner])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("0", parsed["current_context"])

    def test_empty_list_returns_empty_dict(self):
        ctx = Context(storage=[])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(parsed["current_context"], {})

    def test_tuple_storage(self):
        ctx = Context(storage=({"a": 1}, {"b": 2}))
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(len(parsed["current_context"]), 2)
