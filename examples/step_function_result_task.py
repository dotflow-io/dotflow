#!/usr/bin/env python

from dotflow import DotFlow, action


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()

    for task in workflow.result_task():
        print(task.task_id, task.status, task.current_context.storage)
        assert task.current_context.storage, "ok"

    return workflow


if __name__ == "__main__":
    main()
