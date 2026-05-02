"""Tests for the on_input_change policy in Manager."""

import unittest
from uuid import uuid4

from dotflow import Config, DotFlow, action
from dotflow.core.exception import InputChangedError, InvalidOnInputChange
from dotflow.core.fingerprint import read_fingerprint
from dotflow.providers.storage_default import StorageDefault


@action
def step_one(initial_context):
    return {"value": initial_context.storage["v"]}


def _build(config: Config, payload: dict, workflow_id):
    workflow = DotFlow(config=config, workflow_id=workflow_id)
    workflow.task.add(step=step_one, initial_context=payload)
    return workflow


class TestOnInputChangePolicy(unittest.TestCase):
    def test_invalid_policy_raises(self):
        config = Config(storage=StorageDefault())
        workflow = _build(config, {"v": 1}, str(uuid4()))

        with self.assertRaises(InvalidOnInputChange):
            workflow.start(resume=True, on_input_change="bogus")

    def test_first_run_records_fingerprint(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())
        workflow = _build(config, {"v": 1}, workflow_id)

        workflow.start(resume=True)

        self.assertIsNotNone(
            read_fingerprint(storage=config.storage, workflow_id=workflow_id)
        )

    def test_same_input_keeps_same_fingerprint(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(resume=True)
        first_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        _build(config, {"v": 1}, workflow_id).start(resume=True)
        second_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        self.assertEqual(first_fp, second_fp)

    def test_changed_input_with_raise_policy_throws(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(resume=True)

        with self.assertRaises(InputChangedError):
            _build(config, {"v": 2}, workflow_id).start(
                resume=True,
                on_input_change="raise",
            )

    def test_changed_input_with_reset_policy_replaces_fingerprint(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(resume=True)
        first_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        _build(config, {"v": 2}, workflow_id).start(
            resume=True,
            on_input_change="reset",
        )
        second_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        self.assertNotEqual(first_fp, second_fp)

    def test_changed_input_with_reuse_policy_keeps_old_fingerprint(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(resume=True)
        first_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        _build(config, {"v": 2}, workflow_id).start(
            resume=True,
            on_input_change="reuse",
        )
        second_fp = read_fingerprint(
            storage=config.storage,
            workflow_id=workflow_id,
        )

        self.assertEqual(first_fp, second_fp)

    def test_no_resume_skips_fingerprint(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(resume=False)

        self.assertIsNone(
            read_fingerprint(storage=config.storage, workflow_id=workflow_id)
        )

    def test_explicit_fingerprint_overrides_payload_hash(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(
            resume=True,
            fingerprint="custom-fp",
        )

        self.assertEqual(
            read_fingerprint(storage=config.storage, workflow_id=workflow_id),
            "custom-fp",
        )

    def test_explicit_fingerprint_makes_payload_changes_invisible(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(
            resume=True,
            fingerprint="stable",
        )

        _build(config, {"v": 2}, workflow_id).start(
            resume=True,
            fingerprint="stable",
            on_input_change="raise",
        )

        self.assertEqual(
            read_fingerprint(storage=config.storage, workflow_id=workflow_id),
            "stable",
        )

    def test_explicit_fingerprint_change_triggers_raise(self):
        config = Config(storage=StorageDefault())
        workflow_id = str(uuid4())

        _build(config, {"v": 1}, workflow_id).start(
            resume=True,
            fingerprint="fp-a",
        )

        with self.assertRaises(InputChangedError):
            _build(config, {"v": 1}, workflow_id).start(
                resume=True,
                fingerprint="fp-b",
                on_input_change="raise",
            )
