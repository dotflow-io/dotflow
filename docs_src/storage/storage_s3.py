from dotflow import Config, DotFlow, action
from dotflow.providers import StorageS3


@action
def step_one():
    return {"message": "hello from S3"}


@action
def step_two(previous_context):
    print(previous_context.storage)
    return "ok"


config = Config(
    storage=StorageS3(
        bucket="dotflow-io-bucket",
        prefix="workflows/",
        region="us-east-1",
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
