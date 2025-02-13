#!/usr/bin/env python

from dotflow import DotFlow, action, retry


def callback(**kwargs):
    print(kwargs)


@action
@retry(max_retry=1)
def my_task():
    print("task")
    raise Exception("Task Error!")


def main():
    workflow = DotFlow()

    workflow.task.add(step=my_task, callback=callback)
    workflow.task.add(step=my_task, callback=callback)
    workflow.task.add(step=my_task)

    workflow.start(workflow=workflow)


if __name__ == '__main__':
    main()
