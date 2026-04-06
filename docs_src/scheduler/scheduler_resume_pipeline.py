from dotflow import Config, DotFlow, action
from dotflow.providers import SchedulerCron, StorageFile


@action
def extract():
    return {"records": fetch_from_api()}


@action
def transform(previous_context):
    data = previous_context.storage["records"]
    return {"cleaned": clean(data)}


@action
def load(previous_context):
    save_to_database(previous_context.storage["cleaned"])
    return {"loaded": True}


def main():
    config = Config(
        storage=StorageFile(),
        scheduler=SchedulerCron(cron="0 6 * * *", overlap="skip"),
    )

    workflow = DotFlow(config=config, workflow_id="etl-daily")
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.task.add(step=load)
    workflow.schedule(mode="sequential", resume=True)


if __name__ == "__main__":
    main()
