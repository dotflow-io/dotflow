from dotflow import Config, DotFlow, action
from dotflow.providers import LogDefault


@action
def extract():
    return {"data": "fetched"}


@action
def transform(previous_context):
    return {"result": previous_context.storage}


def main():
    log = LogDefault(
        level="INFO",
        output="console",
        format="simple",
    )

    workflow = DotFlow(config=Config(log=log))
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
