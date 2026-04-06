from dotflow import Config, DotFlow, action
from dotflow.core.types.status import TypeStatus
from dotflow.providers import NotifyTelegram, StorageFile


@action
def extract():
    return {"data": fetch_data()}


@action
def transform(previous_context):
    return {"result": process(previous_context.storage)}


@action
def load(previous_context):
    save(previous_context.storage)
    return {"loaded": True}


def main():
    config = Config(
        storage=StorageFile(),
        notify=NotifyTelegram(
            token="YOUR_BOT_TOKEN",
            chat_id=123456789,
            notification_type=TypeStatus.FAILED,
        ),
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.task.add(step=load)
    workflow.start()


if __name__ == "__main__":
    main()
