from dotflow import DotFlow, action
from dotflow.core.types.status import TypeStatus


def callback_one(tasks):
    assert tasks
    assert len(tasks)

    for task in tasks:
        assert task.status is TypeStatus.COMPLETED
        print(task.task_id, task.status, task.current_context.storage)


def callback_two(tasks):
    assert tasks
    assert len(tasks)

    for task in tasks:
        assert task.status is TypeStatus.FAILED
        print(task.task_id, task.status, task.current_context.storage)


@action
def simple_one():
    raise "ok"

@action
def simple_two():
    raise Exception("Fail!")


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_one, callback=callback_one)
    workflow.task.add(step=simple_two, callback=callback_two)
    workflow.start(keep_going=True)

    return workflow


if __name__ == "__main__":
    main()
