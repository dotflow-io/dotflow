from dotflow import Config, DotFlow, action
from dotflow.providers import SchedulerDefault


@action
def task():
    return {"scheduled": True}


def main():
    workflow = DotFlow(config=Config(scheduler=SchedulerDefault()))
    workflow.task.add(step=task)

    return workflow


if __name__ == "__main__":
    main()
