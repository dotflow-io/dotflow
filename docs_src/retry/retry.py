from dotflow import DotFlow, action


@action(retry=5)
def simple_step():
    raise Exception("Unknown")


@action
class SimpleStepX:

    @action(retry=5)
    def run(self):
        raise Exception("Unknown")


@action(retry=3)
class SimpleStepY:

    @action
    def run(self):
        raise Exception("Unknown")


def main():
    workflow = DotFlow()

    workflow.add(step=simple_step)
    workflow.start()
    workflow.task.clear()

    workflow.add(step=SimpleStepX)
    workflow.start()
    workflow.task.clear()

    workflow.add(step=SimpleStepY)
    workflow.start()
    workflow.task.clear()

    return workflow


if __name__ == "__main__":
    main()
