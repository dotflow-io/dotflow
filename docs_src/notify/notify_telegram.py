import os

from dotenv import load_dotenv

from dotflow import Config, DotFlow, action
from dotflow.core.types.status import TypeStatus
from dotflow.providers import NotifyTelegram


@action
def step_one():
    return {"data": "processed"}


@action
def step_two():
    raise RuntimeError("Fail!")


def main():
    load_dotenv()

    notify = NotifyTelegram(
        token=os.getenv("BOT_TOKEN", ""),
        chat_id=int(os.getenv("CHAT_ID", "0")),
        notification_type=TypeStatus.FAILED,
        show_result=True,
    )

    workflow = DotFlow(config=Config(notify=notify))
    workflow.task.add(step=step_one)
    workflow.task.add(step=step_two)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
