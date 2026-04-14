from os import system

from dotflow import action


@action
def simple_step():
    return "ok"


def main():
    system(
        "dotflow start --step docs_src.cli.cli_with_path:simple_step "
        "--path .storage --storage file"
    )

    system(
        "dotflow start --step docs_src.cli.cli_with_path:simple_step "
        "--path . --storage file"
    )


if __name__ == "__main__":
    main()
