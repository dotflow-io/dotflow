from dotflow import DotFlow, action


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.add(step=simple_step)
    workflow.start()

    for context in workflow.result_context():
        print(context.time, context.storage)
        assert context.storage == "ok"

    return workflow


if __name__ == "__main__":
    main()
