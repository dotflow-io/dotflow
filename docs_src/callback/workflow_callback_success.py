from typing import List

from dotflow import DotFlow, action, Task
from dotflow.core.types.status import StatusTaskType


def callback(tasks: List[Task]):
    assert tasks
    assert len(tasks)

    for task in tasks:
        assert task.status is StatusTaskType.COMPLETED
        print(task.task_id, task.status, task.current_context.storage)


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.add(step=simple_step)
    workflow.start(on_success=callback)

    return workflow


if __name__ == "__main__":
    main()
