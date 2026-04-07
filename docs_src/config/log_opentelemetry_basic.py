from dotflow import Config, DotFlow, action
from dotflow.providers import LogOpenTelemetry


@action
def extract():
    return {"data": "fetched"}


@action
def transform(previous_context):
    return {"result": previous_context.storage}


def main():
    config = Config(
        log=LogOpenTelemetry(service_name="my-pipeline", output="console"),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
