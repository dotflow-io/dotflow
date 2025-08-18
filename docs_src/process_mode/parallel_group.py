from time import sleep

from dotflow import DotFlow, action, Context


@action
def task_foo(initial_context: Context):
    sleep(2)
    value = initial_context.storage
    return value * value * value


@action
def task_bar(initial_context: Context):
    sleep(1)
    value = initial_context.storage
    return value * value * value


def main():
    workflow = DotFlow()

    workflow.add(step=task_foo, initial_context=10, group_name="foo")
    workflow.add(step=task_bar, initial_context=10, group_name="bar")

    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
