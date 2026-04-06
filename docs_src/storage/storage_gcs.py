from dotflow import Config, DotFlow, action
from dotflow.providers import StorageGCS


@action
def step_one():
    return {"message": "hello from GCS"}


@action
def step_two(previous_context):
    print(previous_context.storage)
    return "ok"


config = Config(
    storage=StorageGCS(
        bucket="dotflow-io-bucket",
        prefix="workflows/",
        project="etl-test",
    )
)


def main():
    workflow = DotFlow(config=config)

    workflow.task.add(step=step_one)
    workflow.task.add(step=step_two)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
