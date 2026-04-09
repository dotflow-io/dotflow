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
