from os import system

from dotflow import DotFlow, action


@action
def step_one():
    return "step one done"


@action
def step_two():
    return "step two done"


def pipeline() -> DotFlow:
    workflow = DotFlow()
    workflow.task.add(step=step_one)
    workflow.task.add(step=step_two)

    return workflow


def main():
    system(
        "dotflow start --step docs_src.cli.cli_with_workflow:step_one"
    )
    system(
        "dotflow start --workflow docs_src.cli.cli_with_workflow:pipeline"
    )
    system(
        "dotflow start --workflow docs_src.cli.cli_with_workflow:pipeline"
        " --mode parallel"
    )


if __name__ == "__main__":
    main()
