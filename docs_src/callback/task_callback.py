from dotflow import DotFlow, action, Task
from dotflow.core.types.task import StatusTaskType


def callback_one(task: Task):
    assert task.status is StatusTaskType.SUCCESS
    print(task.task_id, task.status, task.current_context.storage)


def callback_two(task: Task):
    assert task.status is StatusTaskType.FAILED
    print(task.task_id, task.status, task.current_context.storage)


@action
def simple_one():
    return "ok"


@action
def simple_two():
    raise Exception("Fail!")


def main():
    workflow = DotFlow()

    workflow.add(step=simple_one, callback=callback_one)
    workflow.add(step=simple_two, callback=callback_two)
    workflow.start(keep_going=True)

    return workflow


if __name__ == "__main__":
    main()
