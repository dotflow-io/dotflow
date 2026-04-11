from dotflow import DotFlow, action


@action
def step_a():
    return {"group": "A", "step": 1}


@action
def step_b(previous_context):
    return {"group": "A", "step": 2}


@action
def step_c():
    return {"group": "B", "step": 1}


@action
def step_d(previous_context):
    return {"group": "B", "step": 2}


def main():
    workflow = DotFlow()

    workflow.task.add(step=step_a, group_name="group_a")
    workflow.task.add(step=step_b, group_name="group_a")
    workflow.task.add(step=step_c, group_name="group_b")
    workflow.task.add(step=step_d, group_name="group_b")

    workflow.start(mode="sequential_group")

    return workflow


if __name__ == "__main__":
    main()
