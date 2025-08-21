from dotflow import DotFlow, action
from dotflow.plugins import MetricsHandler


@action
def my_task():
    print("task")


def main():
    workflow = DotFlow(plugins=MetricsHandler)

    workflow.add(step=my_task)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
