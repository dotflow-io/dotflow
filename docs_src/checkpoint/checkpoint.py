from dotflow import Config, DotFlow, action
from dotflow.providers import StorageFile


@action
def step_one():
    return {"extracted": True}


@action
def step_two(previous_context):
    return {"transformed": previous_context.storage}


@action
def step_three(previous_context):
    return {"loaded": previous_context.storage}


config = Config(storage=StorageFile())


def main():
    workflow = DotFlow(config=config, workflow_id="my-etl-pipeline")

    workflow.task.add(step=step_one)
    workflow.task.add(step=step_two)
    workflow.task.add(step=step_three)
    workflow.start(mode="sequential", resume=True)

    return workflow


if __name__ == "__main__":
    main()
