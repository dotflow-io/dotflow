from dotflow import Config, DotFlow, action
from dotflow.providers import LogDefault, NotifyDefault, StorageFile


@action
def extract():
    return {"status": "ok"}


def main():
    config = Config(
        storage=StorageFile(path=".output"),
        notify=NotifyDefault(),
        log=LogDefault(),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
