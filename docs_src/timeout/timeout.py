from time import sleep

from dotflow import DotFlow, action


@action(timeout=3)
def simple_step():
    sleep(5)


@action
class SimpleStepX:

    @action(timeout=3)
    def run(self):
        sleep(5)


@action(timeout=3)
class SimpleStepY:

    def __init__(self):
        sleep(5)


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
