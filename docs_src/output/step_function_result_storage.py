from dotflow import DotFlow, action


@action
def simple_step():
    return "ok"


def main():
    workflow = DotFlow()

    workflow.add(step=simple_step)
    workflow.start()

    for storage in workflow.result_storage():
        print(storage)
        assert storage == "ok"

    return workflow


if __name__ == "__main__":
    main()
