from dotflow import Config, DotFlow, action
from dotflow.providers import SchedulerCron


@action
def extract():
    return {"data": "fetched"}


@action
def load(previous_context):
    return {"saved": previous_context.storage}


def main():
    config = Config(
        scheduler=SchedulerCron(cron="*/1 * * * *"),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=load)
    workflow.schedule()


if __name__ == "__main__":
    main()
