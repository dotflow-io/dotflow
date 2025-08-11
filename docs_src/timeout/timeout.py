from time import sleep

from dotflow import DotFlow, action


@action(timeout=3)  # HERE
def simple_step():
    sleep(5)


@action
class SimpleStepX:

    @action(timeout=3)  # HERE
    def run(self):
        sleep(5)


@action(timeout=3)  # HERE
class SimpleStepY:

    def __init__(self):
        sleep(5)


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
