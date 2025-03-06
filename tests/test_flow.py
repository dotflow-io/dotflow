#!/usr/bin/env python

from dotflow import DotFlow, action


@action(retry=5)
class StepX:

    @action
    def first_function(self):
        return {"foo": "bar"}

    @action
    def second_function(self):
        return True


@action(retry=5)
class StepY:

    def __init__(self, initial_context):
        print(initial_context.storage, "__init__")
        assert initial_context.storage
        self.variable = True

    def auxiliary_function(self):
        """This function will not be executed, because
        it does not have an 'action' decorator.
        """

    @action
    def first_function(self, initial_context):
        print(initial_context.storage, "first_function")
        assert initial_context.storage
        assert self.variable

        return {"foo": "bar"}

    @action
    def second_function(self, previous_context):
        print(previous_context.storage, "second_function")
        assert previous_context.storage

        return True


@action
def simple_step():
    return "ok"


@action
def extract_task_x():
    return "extract"


@action
def transform_task_x(initial_context, previous_context):
    print(initial_context.storage, "initial_context")
    print(previous_context.storage, "previous_context")

    assert initial_context.storage, {"foo": True}
    assert previous_context.storage, "extract"

    return "transform"


@action
def load_task_x():
    return "load"


@action
def extract_task_y():
    print("extract")
    return "extract"


@action
def transform_task_y(previous_context):
    print(previous_context.storage, "transform")
    assert previous_context.storage, "extract"

    return "transform"


@action
def load_task_y(previous_context):
    print(previous_context.storage, "load")
    assert previous_context.storage, "transform"

    return "load"


def main():
    workflow = DotFlow()

    workflow.task.add(step=StepX)
    workflow.task.add(step=StepY, initial_context={"foo": "bar"})
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=simple_step)
    workflow.task.add(step=extract_task_x)
    workflow.task.add(step=transform_task_x, initial_context={"foo": True})
    workflow.task.add(step=load_task_x)
    workflow.task.add(step=extract_task_y)
    workflow.task.add(step=transform_task_y)
    workflow.task.add(step=load_task_y)
    workflow.start()

    workflow = DotFlow()
    workflow.task.add(
        [
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
            simple_step,
        ],
        initial_context={"foo": "bar"}
    )
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
