"""Tests for SerializerWorkflow computed fields."""

from uuid import uuid4

from dotflow.core.serializers.workflow import SerializerWorkflow


def test_id_mirrors_workflow_id():
    wid = uuid4()
    payload = SerializerWorkflow(
        workflow_id=wid, workflow_name="host-a"
    ).model_dump()

    assert payload["workflow_id"] == wid
    assert payload["id"] == wid


def test_name_mirrors_workflow_name():
    payload = SerializerWorkflow(
        workflow_id=uuid4(), workflow_name="host-b"
    ).model_dump()

    assert payload["workflow_name"] == "host-b"
    assert payload["name"] == "host-b"


def test_name_is_none_when_not_set():
    payload = SerializerWorkflow(workflow_id=uuid4()).model_dump()
    assert payload["workflow_name"] is None
    assert payload["name"] is None
