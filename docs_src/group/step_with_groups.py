from time import sleep

from dotflow import DotFlow, action


@action
def task_foo():
    sleep(5)
    print("2: Task Foo")
    return "ok"


@action
def task_bar():
    sleep(2)
    print("1: Task Bar")
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=task_foo, group_name="foo")
    workflow.task.add(step=task_bar, group_name="bar")
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
