"""Test SerializerTask model_dump_json"""

import json
import unittest

from dotflow.core.context import Context
from dotflow.core.serializers.task import SerializerTask


class TestSerializerTaskDumpJson(unittest.TestCase):
    def _make_task(self, **kwargs):
        defaults = {
            "task_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
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
        self.assertEqual(parsed["task_id"], "01ARZ3NDEKTSV4RRFFQ69G5FAV")
        self.assertEqual(parsed["status"], "Completed")

    def test_with_max_does_not_mutate_self(self):
        ctx = Context(storage={"large": "x" * 500})
        task = self._make_task(_initial_context=ctx, max=100)

        task.model_dump_json()
        task.model_dump_json()

        self.assertIsNotNone(task.initial_context)

    def test_with_max_returns_valid_json(self):
        ctx = Context(storage={"large": "x" * 500})
        task = self._make_task(_initial_context=ctx, max=100)

        result = task.model_dump_json()
        json.loads(result)

    def test_with_max_truncates_largest_context_first(self):
        task = self._make_task(
            _initial_context=Context(storage={"small": "x" * 10}),
            _current_context=Context(storage={"large": "y" * 500}),
            _previous_context=Context(storage={"medium": "z" * 100}),
            max=500,
        )

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertEqual(
            parsed["current_context"],
            {"message": "Context size exceeded"},
        )
        self.assertNotEqual(
            parsed["initial_context"],
            {"message": "Context size exceeded"},
        )

    def test_with_max_truncates_all_contexts_if_needed(self):
        task = self._make_task(
            _initial_context=Context(storage={"large": "x" * 500}),
            _current_context=Context(storage={"large": "y" * 500}),
            _previous_context=Context(storage={"large": "z" * 500}),
            max=600,
        )

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertEqual(
            parsed["initial_context"],
            {"message": "Context size exceeded"},
        )
        self.assertEqual(
            parsed["current_context"],
            {"message": "Context size exceeded"},
        )
        self.assertEqual(
            parsed["previous_context"],
            {"message": "Context size exceeded"},
        )

    def test_with_max_very_small_nullifies_contexts(self):
        task = self._make_task(
            _initial_context=Context(storage={"large": "x" * 500}),
            _current_context=Context(storage={"large": "y" * 500}),
            max=100,
        )

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertIsNone(parsed["initial_context"])
        self.assertIsNone(parsed["current_context"])

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
        task = self._make_task(_errors=large_errors, max=500)

        result = task.model_dump_json()
        parsed = json.loads(result)
        self.assertLessEqual(len(result), 500)

        self.assertEqual(parsed["errors"], [])
        self.assertIsNone(parsed["error"])

    def test_with_max_zero_truncates(self):
        ctx = Context(storage={"data": "x" * 500})
        task = self._make_task(_current_context=ctx, max=0)

        result = task.model_dump_json()
        parsed = json.loads(result)

        self.assertEqual(
            parsed["current_context"],
            {"message": "Context size exceeded"},
        )

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
        self.assertIn("raw:0", parsed["current_context"])
        self.assertIn("raw:1", parsed["current_context"])

    def test_list_of_context_objects(self):
        inner_a = Context(
            storage={"name": "a"},
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        )
        inner_b = Context(
            storage={"name": "b"},
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAW",
        )
        ctx = Context(storage=[inner_a, inner_b])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("01ARZ3NDEKTSV4RRFFQ69G5FAV", parsed["current_context"])
        self.assertIn("01ARZ3NDEKTSV4RRFFQ69G5FAW", parsed["current_context"])

    def test_list_mixed_context_and_raw(self):
        inner = Context(
            storage={"nested": True},
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        )
        ctx = Context(storage=[inner, {"raw": True}])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("01ARZ3NDEKTSV4RRFFQ69G5FAV", parsed["current_context"])
        self.assertIn("raw:1", parsed["current_context"])

    def test_list_context_without_task_id(self):
        inner = Context(storage={"data": True})
        inner._task_id = None
        ctx = Context(storage=[inner])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("ctx:0", parsed["current_context"])

    def test_context_task_id_none_no_collision(self):
        ctx_none = Context(storage={"step": "extract"})
        ctx_none._task_id = None
        ctx_ulid = Context(
            storage={"step": "transform"},
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        )
        ctx = Context(storage=[ctx_none, ctx_ulid])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("ctx:0", parsed["current_context"])
        self.assertIn("01ARZ3NDEKTSV4RRFFQ69G5FAV", parsed["current_context"])
        self.assertEqual(len(parsed["current_context"]), 2)

    def test_empty_list_returns_empty_dict(self):
        ctx = Context(storage=[])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(parsed["current_context"], {})

    def test_mixed_list_no_key_collision(self):
        raw_item = {"users": 150}
        context_item = Context(
            storage={"status": "done"},
            task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        )
        ctx = Context(storage=[raw_item, context_item])
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertIn("raw:0", parsed["current_context"])
        self.assertIn("01ARZ3NDEKTSV4RRFFQ69G5FAV", parsed["current_context"])
        self.assertEqual(len(parsed["current_context"]), 2)

    def test_tuple_storage(self):
        ctx = Context(storage=({"a": 1}, {"b": 2}))
        task = self._make_task(_current_context=ctx)

        parsed = json.loads(task.model_dump_json())
        self.assertEqual(len(parsed["current_context"]), 2)
