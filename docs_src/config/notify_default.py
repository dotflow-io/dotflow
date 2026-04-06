from dotflow import Config, DotFlow, action
from dotflow.providers import NotifyDefault


@action
def task():
    return {"notify": True}


def main():
    workflow = DotFlow(config=Config(notify=NotifyDefault()))
    workflow.task.add(step=task)

    return workflow


if __name__ == "__main__":
    main()
