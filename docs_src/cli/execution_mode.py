from os import system

from dotflow import action


@action
def simple_step():
    return "ok"


def main():
    """
    COMMAND:
        dotflow start --step docs_src.cli.execution_mode.simple_step --mode sequential
        dotflow start --step docs_src.cli.execution_mode.simple_step --mode background

    OUTPUT:
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - In queue
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - In progress
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - Success
    """

    system("dotflow start --step docs_src.cli.execution_mode.simple_step --mode sequential")
    system("dotflow start --step docs_src.cli.execution_mode.simple_step --mode background")


if __name__ == "__main__":
    main()
