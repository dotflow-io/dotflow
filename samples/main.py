#!/usr/bin/env python

from dotflow import (
    action,
    Context,
    Executor,
    Task,
    Workflow
)


class Extract(Task):

    @action
    def run(self):
        return "ok"


class Transform(Task):

    @action
    def run(self):
        return Context(storage=True)


class Load(Task):

    @action
    def run(self):
        pass


class MyWorkflow(Workflow):

    def build(self) -> None:
        return self.builder.add(
            step=Extract
        ).add(
            step=Transform,
        ).add(
            step=Load
        )


def main():
    result = Executor.start(workflow=MyWorkflow())

    for item in result:
        print(item.status, ":", item.current_context.storage)


if __name__ == '__main__':
    main()
