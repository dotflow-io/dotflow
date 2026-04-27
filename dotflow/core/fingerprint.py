"""Input fingerprint helpers for resume + on_input_change policy."""

from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any

from dotflow.core.context import Context

FP_KEY_SUFFIX = "-_input_fp"
VALID_POLICIES = ("reuse", "reset", "raise")


def fingerprint_of(values: list[Any]) -> str:
    """SHA256 of JSON-serialized list of initial_context payloads.

    Inputs must be JSON-serializable (primitives, lists, dicts).
    Non-serializable objects fall back to ``repr``, which is **not**
    guaranteed to be stable across processes — objects without a custom
    ``__repr__`` will produce different fingerprints on every run because
    the default repr embeds the memory address.
    """
    try:
        encoded = dumps(values, sort_keys=True)
    except (TypeError, ValueError):
        encoded = repr(values)

    return sha256(encoded.encode("utf-8")).hexdigest()


def fp_key(workflow_id: str) -> str:
    return f"{workflow_id}{FP_KEY_SUFFIX}"


def read_fingerprint(storage, workflow_id: str) -> str | None:
    context = storage.get(key=fp_key(workflow_id))

    if isinstance(context, Context) and isinstance(context.storage, str):
        return context.storage

    return None


def write_fingerprint(storage, workflow_id: str, value: str) -> None:
    storage.post(key=fp_key(workflow_id), context=Context(storage=value))
