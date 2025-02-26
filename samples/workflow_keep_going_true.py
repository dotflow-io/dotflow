#!/usr/bin/env python

from dotflow import DotFlow, action


@action
def extract_task():
    return "extract"


@action
def transform_task(previous_context):
    print(previous_context.storage, "transform")
    raise Exception("Fail!")


@action
def load_task(previous_context):
    print(previous_context.storage, "load")
    return "load"


def main():
    workflow = DotFlow()

    workflow.task.add(step=extract_task)
    workflow.task.add(step=transform_task)
    workflow.task.add(step=load_task)

    workflow.start(keep_going=True)  # HERE

    for task in workflow.task.queu:
        print(
            task.task_id,
            task.status,
            task.previous_context.storage,
            ">",
            task.current_context.storage
        )


if __name__ == '__main__':
    main()
