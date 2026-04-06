from dotflow import Config, DotFlow, action
from dotflow.providers import SchedulerCron, SchedulerDefault


@action
def task():
    return {"scheduled": True}


def main():
    workflow_default = DotFlow(config=Config(scheduler=SchedulerDefault()))
    workflow_default.task.add(step=task)

    workflow_cron = DotFlow(
        config=Config(
            scheduler=SchedulerCron(cron="0 * * * *"),
        )
    )
    workflow_cron.task.add(step=task)

    return workflow_default, workflow_cron


if __name__ == "__main__":
    main()
