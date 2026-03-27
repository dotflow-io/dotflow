from dotflow import Config, DotFlow, action
from dotflow.providers import LogDefault


@action
def task():
    return {"log": True}


def main():
    # Use built-in logger implementation.
    workflow = DotFlow(config=Config(log=LogDefault()))
    workflow.task.add(step=task)
    workflow.start()
    return workflow


if __name__ == "__main__":
    main()
