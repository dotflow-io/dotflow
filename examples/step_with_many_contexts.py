#!/usr/bin/env python

from dotflow import DotFlow, action


@action
def extract_task():
    return "extract"


@action
def transform_task(initial_context, previous_context):  # HERE
    print(initial_context.storage, "initial_context")
    print(previous_context.storage, "previous_context")

    assert initial_context.storage
    assert previous_context.storage

    return "transform"


@action
def load_task():
    return "load"


def main():
    workflow = DotFlow()

    workflow.task.add(step=extract_task)
    workflow.task.add(step=transform_task, initial_context={"foo": True})
    workflow.task.add(step=load_task)

    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
