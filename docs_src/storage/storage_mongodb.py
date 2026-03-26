from dotflow import Config, DotFlow, action
from dotflow.storage import StorageMongoDB


@action
def simple_step():
    return "ok"


def main():
    config = Config(storage=StorageMongoDB())

    workflow = DotFlow(config=config)
    workflow.task.add(step=simple_step)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
