from dotflow import DotFlow, action
from dotflow.plugins import LogsHandler


@action
def my_task():
    print("task")


def main():
    workflow = DotFlow(plugins=LogsHandler)

    workflow.add(step=my_task)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
