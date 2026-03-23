from dotflow import Config, DotFlow, action
from dotflow.providers import StorageFile


@action
def simple_step():
    return "ok"


def main():
    config = Config(storage=StorageFile(path=".output"))

    workflow = DotFlow(config=config)
    workflow.task.add(step=simple_step)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
