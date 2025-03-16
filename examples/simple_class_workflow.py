#!/usr/bin/env python

from dotflow import DotFlow, action


@action(retry=5)
class Step:

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
        assert initial_context.storage == {"foo": "bar"}
        assert self.variable is True

        return {"foo": "bar"}

    @action
    def second_function(self, previous_context):
        print(previous_context.storage, "second_function")
        assert previous_context.storage == {"foo": "bar"}

        return True


def main():
    workflow = DotFlow()

    workflow.task.add(step=Step, initial_context={"foo": "bar"})
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
