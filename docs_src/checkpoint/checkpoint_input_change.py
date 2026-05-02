from hashlib import sha256
from uuid import UUID

from dotflow import Config, DotFlow, action
from dotflow.providers import StorageFile


@action
def step_one(initial_context):
    return {"loaded": initial_context.storage}


@action
def step_two(previous_context):
    return {"transformed": previous_context.storage}


config = Config(storage=StorageFile())


def main():
    payload = {"s3_key": "uploads/data.zip", "v": 1}

    workflow = DotFlow(
        config=config,
        workflow_id=UUID("12345678-1234-5678-1234-567812345678"),
    )

    workflow.task.add(step=[step_one, step_two], initial_context=payload)

    fp = sha256(payload["s3_key"].encode()).hexdigest()
    workflow.start(resume=True, on_input_change="reset", fingerprint=fp)

    return workflow


if __name__ == "__main__":
    main()
