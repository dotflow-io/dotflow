from dotflow import DotFlow, action


@action
def extract_task(initial_context):
    print(initial_context.storage, "extract")
    assert initial_context.storage == {"foo": True}

    return "extract"


@action
def transform_task(initial_context):
    print(initial_context.storage, "transform")
    assert initial_context.storage == {"bar": True}

    return "transform"


@action
def load_task():
    return "load"


def main():
    workflow = DotFlow()

    workflow.task.add(step=extract_task, initial_context={"foo": True})
    workflow.task.add(step=transform_task, initial_context={"bar": True})
    workflow.task.add(step=load_task)

    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
