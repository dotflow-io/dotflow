from dotflow import DotFlow, action


@action(retry=3)
def step_with_retry():
    raise ValueError("Something went wrong")


def main():
    workflow = DotFlow()

    workflow.task.add(step=step_with_retry)
    workflow.start()

    for task in workflow.result_task():
        print(f"Retry count: {task.retry_count}")
        print(f"Total errors: {len(task.errors)}")

        for error in task.errors:
            print(f"  Attempt {error.attempt}: [{error.exception}] {error.message}")

    return workflow


if __name__ == "__main__":
    main()
