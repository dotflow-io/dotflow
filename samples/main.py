#!/usr/bin/env python

from dotflow import DotFlow, action


def callback(**kwargs):
    print("Callback", kwargs)


@action(retry=5)
def extract_task():
    print("extract")
    return 1


@action
def transform_task(previous_context):
    print(previous_context.storage, "transform")


@action
def load_task():
    print("load")


def main():
    workflow = DotFlow()

    workflow.task.add(step=extract_task, callback=callback)
    workflow.task.add(step=transform_task, callback=callback)
    workflow.task.add(step=load_task)

    workflow.start(workflow=workflow)


if __name__ == '__main__':
    main()
