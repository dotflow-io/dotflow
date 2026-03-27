from dotflow import Config, DotFlow, action
from dotflow.providers import StorageDefault, StorageFile


@action
def task():
    return {"hello": "dotflow"}


def main():
    # In-memory storage (default-like behavior).
    workflow_memory = DotFlow(config=Config(storage=StorageDefault()))
    workflow_memory.task.add(step=task)
    workflow_memory.start()

    # File storage persisted in ".output/tasks".
    workflow_file = DotFlow(config=Config(storage=StorageFile(path=".output")))
    workflow_file.task.add(step=task)
    workflow_file.start()

    return workflow_memory, workflow_file


if __name__ == "__main__":
    main()
