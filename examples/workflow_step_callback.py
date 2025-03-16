#!/usr/bin/env python

from dotflow import DotFlow, action
from dotflow.core.types.status import TaskStatus


def callback(content):  # HERE
    assert content
    assert content.current_context.storage == "ok"
    assert content.status is TaskStatus.COMPLETED

    print(content.task_id, content.status, content.current_context.storage)
    print(content.__dict__)


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step, callback=callback)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
