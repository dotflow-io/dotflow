from dotflow import DotFlow, action


@action(retry=1, backoff=True)
def simple_step():
    raise Exception("Unknown")


@action
class SimpleStepX:

    @action(retry=1, backoff=True)
    def run(self):
        raise Exception("Unknown")


@action(retry=1, backoff=True)
class SimpleStepY:

    @action
    def run(self):
        raise Exception("Unknown")


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()
    workflow.task.clear()

    workflow.task.add(step=SimpleStepX)
    workflow.start()
    workflow.task.clear()

    workflow.task.add(step=SimpleStepY)
    workflow.start()
    workflow.task.clear()

    return workflow


if __name__ == "__main__":
    main()
