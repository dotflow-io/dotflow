from dotflow import Config, DotFlow, action


@action
def my_task():
    print("task")


def main():
    my_config = Config()

    workflow = DotFlow(config=my_config)
    workflow.add(step=my_task)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
