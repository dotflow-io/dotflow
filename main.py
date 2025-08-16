#!/usr/bin/env python

from time import sleep

from dotflow import DotFlow, action


@action
def task_foo(initial_context):
    sleep(2)
    value = initial_context.storage
    return value * value * value, "foo"


@action
def task_bar(initial_context):
    sleep(1)
    value = initial_context.storage
    return value * value * value, "bar"


def main():
    workflow = DotFlow()

    workflow.task.add(step=task_foo, initial_context=10, group_name="foo")
    workflow.task.add(step=task_bar, initial_context=10, group_name="bar")

    # workflow.start(mode="sequential")
    workflow.start(mode="background")
    # workflow.start(mode="parallel")

    for context in workflow.result_context():
        print(context.storage)

    return workflow


if __name__ == "__main__":
    main()
