"""Workflow with a custom name.

``DotFlow`` accepts an optional ``name`` kwarg that is sent to the managed
server when the workflow is registered. When omitted, the name defaults to
the machine hostname — useful to distinguish runs from different hosts in
the dashboard.
"""

from dotflow import DotFlow, action


@action
def step_one():
    return "done"


def pipeline() -> DotFlow:
    workflow = DotFlow(name="etl-nightly")
    workflow.task.add(step=step_one)

    return workflow


if __name__ == "__main__":
    pipeline().start()
