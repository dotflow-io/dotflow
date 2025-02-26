#!/usr/bin/env python

from dotflow import DotFlow, action


@action(retry=5)  # HERE
def simple_step():
    print("Fail!")
    raise Exception()


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()

    for task in workflow.task.queu:
        print(task.task_id, task.status, task.current_context.storage)


if __name__ == '__main__':
    main()
