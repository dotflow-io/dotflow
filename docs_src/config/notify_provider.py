from dotflow import Config, DotFlow, action
from dotflow.core.types.status import TypeStatus
from dotflow.providers import NotifyDefault, NotifyTelegram


@action
def task():
    return {"notify": True}


def main():
    # No external notifications.
    workflow_default_notify = DotFlow(config=Config(notify=NotifyDefault()))
    workflow_default_notify.task.add(step=task)

    # Telegram notifications only for failed tasks.
    workflow_telegram_notify = DotFlow(
        config=Config(
            notify=NotifyTelegram(
                token="YOUR_BOT_TOKEN",
                chat_id=123456789,
                notification_type=TypeStatus.FAILED,
            )
        )
    )
    workflow_telegram_notify.task.add(step=task)

    return workflow_default_notify, workflow_telegram_notify


if __name__ == "__main__":
    main()
