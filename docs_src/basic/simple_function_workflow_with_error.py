from dotflow import DotFlow, action


@action
def simple_step():
    raise Exception("Fail!")


def main():
    workflow = DotFlow()

    workflow.task.add(step=simple_step)
    workflow.start()

    for task in workflow.result_task():
        if task.errors:
            print(task.errors[-1].message)
            print(task.errors[-1].exception)
            print(task.errors[-1].traceback)

    return workflow


if __name__ == "__main__":
    main()
