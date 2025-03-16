#!/usr/bin/env python

from dotflow import DotFlow, action
from dotflow.core.types.status import TaskStatus


def callback(tasks):  # HERE
    assert tasks
    assert len(tasks)

    for task in tasks:
        assert task.status is TaskStatus.COMPLETED
        print(task.task_id, task.status, task.current_context.storage)


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start(success=callback)

    return workflow


if __name__ == "__main__":
    main()
