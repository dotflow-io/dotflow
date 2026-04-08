from dotflow import Config, DotFlow, action
from dotflow.providers import TracerSentry


@action
def extract():
    return {"data": "fetched"}


@action
def transform(previous_context):
    return {"result": previous_context.storage}


def main():
    config = Config(
        tracer=TracerSentry(
            dsn="https://xxx@sentry.io/123",
            environment="production",
            traces_sample_rate=1.0,
        ),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
