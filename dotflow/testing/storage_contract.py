"""Storage contract suite."""

from __future__ import annotations

import time

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageContract:
    """Mix into a unittest.TestCase and override make_storage."""

    supports_ttl: bool = True

    def make_storage(self) -> Storage:
        raise NotImplementedError

    def setUp(self) -> None:
        self.storage = self.make_storage()

    def test_post_get_roundtrip(self):
        self.storage.post(key="k1", context=Context(storage={"v": 1}))

        result = self.storage.get(key="k1")

        self.assertEqual(result.storage, {"v": 1})

    def test_get_missing_key_returns_empty_context(self):
        result = self.storage.get(key="missing")

        self.assertIsNone(result.storage)

    def test_delete_returns_true_when_present(self):
        self.storage.post(key="k1", context=Context(storage="a"))

        self.assertTrue(self.storage.delete(key="k1"))
        self.assertIsNone(self.storage.get(key="k1").storage)

    def test_delete_returns_false_when_absent(self):
        self.assertFalse(self.storage.delete(key="missing"))

    def test_delete_prefix_returns_count(self):
        self.storage.post(key="wf-1-a", context=Context(storage="a"))
        self.storage.post(key="wf-1-b", context=Context(storage="b"))
        self.storage.post(key="wf-2-c", context=Context(storage="c"))

        removed = self.storage.delete_prefix("wf-1-")

        self.assertEqual(removed, 2)
        self.assertEqual(self.storage.get(key="wf-2-c").storage, "c")

    def test_list_keys_filters_by_prefix(self):
        self.storage.post(key="wf-1-a", context=Context(storage="a"))
        self.storage.post(key="wf-1-b", context=Context(storage="b"))
        self.storage.post(key="wf-2-c", context=Context(storage="c"))

        keys = sorted(self.storage.list_keys("wf-1-"))

        self.assertEqual(keys, ["wf-1-a", "wf-1-b"])

    def test_atomic_swap_succeeds_when_expected_matches(self):
        self.storage.post(key="k", context=Context(storage="old"))

        ok = self.storage.atomic_swap(key="k", expected="old", new="new")

        self.assertTrue(ok)
        self.assertEqual(self.storage.get(key="k").storage, "new")

    def test_atomic_swap_fails_when_expected_does_not_match(self):
        self.storage.post(key="k", context=Context(storage="old"))

        ok = self.storage.atomic_swap(
            key="k",
            expected="other",
            new="new",
        )

        self.assertFalse(ok)
        self.assertEqual(self.storage.get(key="k").storage, "old")

    def test_atomic_swap_clears_inherited_ttl(self):
        if not self.supports_ttl:
            self.skipTest("driver does not support TTL")

        self.storage.post(key="k", context=Context(storage="old"), ttl=1)

        ok = self.storage.atomic_swap(key="k", expected="old", new="new")

        self.assertTrue(ok)

        time.sleep(1.2)

        self.assertEqual(self.storage.get(key="k").storage, "new")

    def test_atomic_swap_applies_new_ttl(self):
        if not self.supports_ttl:
            self.skipTest("driver does not support TTL")

        self.storage.post(key="k", context=Context(storage="old"))

        ok = self.storage.atomic_swap(
            key="k",
            expected="old",
            new="new",
            ttl=1,
        )

        self.assertTrue(ok)
        self.assertEqual(self.storage.get(key="k").storage, "new")

        time.sleep(1.2)

        self.assertIsNone(self.storage.get(key="k").storage)

    def test_ttl_expiration(self):
        if not self.supports_ttl:
            self.skipTest("driver does not support TTL")

        self.storage.post(key="k", context=Context(storage="x"), ttl=1)

        self.assertEqual(self.storage.get(key="k").storage, "x")

        time.sleep(1.1)

        self.assertIsNone(self.storage.get(key="k").storage)

    def test_clear_delegates_to_delete_prefix(self):
        self.storage.post(key="wf-A-task-1", context=Context(storage="a"))
        self.storage.post(key="wf-B-task-1", context=Context(storage="c"))

        self.storage.clear(workflow_id="wf-A")

        self.assertIsNone(self.storage.get(key="wf-A-task-1").storage)
        self.assertEqual(self.storage.get(key="wf-B-task-1").storage, "c")
