#!/usr/bin/env python

from dotflow import DotFlow, action


@action
def simple_step():
    raise Exception("Fail!")


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()

    for task in workflow.result_task():
        print(task.error.message)
        print(task.error.exception)
        print(task.error.traceback)

    return workflow


if __name__ == "__main__":
    main()
