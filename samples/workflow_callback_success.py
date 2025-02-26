#!/usr/bin/env python

from dotflow import DotFlow, action


def callback(content):  # HERE
    for task in content:
        print(task.task_id, task.status, task.current_context.storage)


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start(success=callback)


if __name__ == '__main__':
    main()
