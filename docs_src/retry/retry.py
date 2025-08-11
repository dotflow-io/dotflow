from dotflow import DotFlow, action


class TestException(Exception):
    def __init__(self):
        super(TestException, self).__init__("Unknown")


@action(retry=5)  # HERE
def simple_step():
    raise TestException()


@action
class SimpleStepX:

    @action(retry=5)  # HERE
    def run(self):
        raise TestException()


@action(retry=3)  # HERE
class SimpleStepY:

    @action
    def run(self):
        raise TestException()


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()

    assert isinstance(workflow.task.queue[0].error.exception, TestException)
    workflow.task.clear()

    workflow.task.add(step=SimpleStepX)
    workflow.start()

    assert isinstance(workflow.task.queue[0].error.exception, TestException)
    workflow.task.clear()

    workflow.task.add(step=SimpleStepY)
    workflow.start()

    assert isinstance(workflow.task.queue[0].error.exception, TestException)
    workflow.task.clear()

    return workflow


if __name__ == "__main__":
    main()
