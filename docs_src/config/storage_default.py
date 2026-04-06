from dotflow import Config, DotFlow, action
from dotflow.providers import StorageDefault


@action
def task():
    return {"hello": "dotflow"}


def main():
    workflow = DotFlow(config=Config(storage=StorageDefault()))
    workflow.task.add(step=task)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
