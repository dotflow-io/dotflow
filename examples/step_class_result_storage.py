#!/usr/bin/env python

from dotflow import DotFlow, action


@action(retry=5)
class Step:

    def __init__(self):
        """It is extremely important to have an '__init__' function!"""

    def auxiliary_function(self):
        """This function will not be executed, because
        it does not have an 'action' decorator.
        """

    @action
    def first_function(self):
        return {"foo": "bar"}

    @action
    def second_function(self):
        return True


def main():
    workflow = DotFlow()

    workflow.task.add(step=Step)
    workflow.start()

    for storages in workflow.result_storage():
        for storage in storages:
            print(storage.time, storage.storage)
            assert storage.storage

    return workflow


if __name__ == "__main__":
    main()
