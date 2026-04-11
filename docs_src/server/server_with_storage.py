"""
Server provider with storage and server combined.

Sends execution data to dotflow-api while
persisting context to local files.
"""

from dotflow import Config, DotFlow, action
from dotflow.providers import ServerDefault, StorageFile


@action
def step_one():
    return {"status": "ok"}


@action
def step_two(previous_context):
    return {"received": previous_context.storage}


def main():
    config = Config(
        storage=StorageFile(path=".output"),
        server=ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="your-api-token",
        ),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=step_one)
    workflow.task.add(step=step_two)

    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
