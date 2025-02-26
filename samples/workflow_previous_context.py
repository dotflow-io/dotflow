#!/usr/bin/env python

from dotflow import DotFlow, action


@action
def extract_task():
    return "extract"


@action
def transform_task(previous_context):   # HERE
    print(previous_context.storage, "transform")
    return "transform"


@action
def load_task(previous_context):   # HERE
    print(previous_context.storage, "load")
    return "load"


def main():
    workflow = DotFlow()

    workflow.task.add(step=extract_task)
    workflow.task.add(step=transform_task)
    workflow.task.add(step=load_task)

    workflow.start()

    for task in workflow.task.queu:
        print(
            task.task_id,
            task.status,
            task.previous_context.storage,  # HERE
            ">",
            task.current_context.storage
        )


if __name__ == '__main__':
    main()
