"""Test input fingerprint helpers."""

import unittest

from dotflow.core.context import Context
from dotflow.core.fingerprint import (
    fingerprint_of,
    fp_key,
    read_fingerprint,
    write_fingerprint,
)
from dotflow.providers.storage_default import StorageDefault


class TestFingerprintOf(unittest.TestCase):
    def test_same_input_same_fingerprint(self):
        a = fingerprint_of([{"k": 1, "z": 2}])
        b = fingerprint_of([{"z": 2, "k": 1}])

        self.assertEqual(a, b)

    def test_different_input_different_fingerprint(self):
        a = fingerprint_of([{"k": 1}])
        b = fingerprint_of([{"k": 2}])

        self.assertNotEqual(a, b)

    def test_falls_back_to_repr_for_non_serializable(self):
        class Custom:
            def __repr__(self):
                return "<Custom>"

        a = fingerprint_of([Custom()])
        b = fingerprint_of([Custom()])

        self.assertEqual(a, b)
        self.assertEqual(len(a), 64)

    def test_none_payload_yields_stable_fingerprint(self):
        a = fingerprint_of([None])
        b = fingerprint_of([None])

        self.assertEqual(a, b)


class TestFingerprintStorage(unittest.TestCase):
    def test_read_returns_none_when_absent(self):
        storage = StorageDefault()

        self.assertIsNone(read_fingerprint(storage=storage, workflow_id="wf"))

    def test_write_then_read_roundtrip(self):
        storage = StorageDefault()
        write_fingerprint(storage=storage, workflow_id="wf", value="abc123")

        self.assertEqual(
            read_fingerprint(storage=storage, workflow_id="wf"),
            "abc123",
        )

    def test_fp_key_is_stable_per_workflow(self):
        self.assertEqual(fp_key("wf"), fp_key("wf"))
        self.assertNotEqual(fp_key("wf-a"), fp_key("wf-b"))

    def test_read_returns_none_for_non_string_storage(self):
        storage = StorageDefault()
        storage.post(key=fp_key("wf"), context=Context(storage={"not": "str"}))

        self.assertIsNone(read_fingerprint(storage=storage, workflow_id="wf"))
