import os
import time

from dotenv import load_dotenv

from dotflow import Config, DotFlow, action
from dotflow.core.types.status import TypeStatus
from dotflow.providers import NotifyTelegram


@action
def simple_step(initial_context):
    time.sleep(0.5)

    return initial_context.storage


@action
def simple_step_raise():
    raise RuntimeError("Fail!")


def main():
    load_dotenv()

    notify = NotifyTelegram(
        token=os.getenv("BOT_TOKEN", ""),
        chat_id=int(os.getenv("CHAT_ID", "0")),
        notification_type=TypeStatus.FAILED,
    )

    workflow = DotFlow(config=Config(notify=notify))
    workflow.task.add(step=simple_step, initial_context={"foo": "bar"})
    workflow.task.add(step=simple_step_raise)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
