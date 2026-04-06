from dotflow import Config, DotFlow, action
from dotflow.providers import SchedulerCron


@action
def heavy_task():
    import time

    time.sleep(120)
    return {"done": True}


def main():
    config_skip = Config(
        scheduler=SchedulerCron(cron="*/5 * * * *", overlap="skip"),
    )

    config_queue = Config(
        scheduler=SchedulerCron(cron="*/5 * * * *", overlap="queue"),
    )

    config_parallel = Config(
        scheduler=SchedulerCron(cron="*/5 * * * *", overlap="parallel"),
    )

    workflow = DotFlow(config=config_skip)
    workflow.task.add(step=heavy_task)
    workflow.schedule()


if __name__ == "__main__":
    main()
