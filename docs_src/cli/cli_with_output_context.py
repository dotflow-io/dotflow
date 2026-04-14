from os import system

from dotflow import action


@action
def simple_step():
    return {"foo": "bar"}


def main():
    system(
        "dotflow start --step docs_src.cli.cli_with_output_context:simple_step "
        "--storage file"
    )


if __name__ == "__main__":
    main()
