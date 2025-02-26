#!/usr/bin/env python

from dotflow import DotFlow, action


def callback(content):  # HERE
    print(content.task_id, content.status, content.current_context.storage)
    print(content.__dict__)


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step, callback=callback)
    workflow.start()


if __name__ == '__main__':
    main()
