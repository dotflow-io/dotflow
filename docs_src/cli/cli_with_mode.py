from os import system

from dotflow import action


@action
def simple_step():
    return "ok"


def main():
    system(
        "dotflow start --step docs_src.cli.cli_with_mode.simple_step --mode sequential"
    )
    system(
        "dotflow start --step docs_src.cli.cli_with_mode.simple_step --mode background"
    )

    system(
        "dotflow start --step docs_src.cli.cli_with_mode.simple_step --mode parallel"
    )


if __name__ == "__main__":
    main()
