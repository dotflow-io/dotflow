from os import system

from dotflow import action


@action
def simple_step(initial_context):
    print(initial_context.storage, "simple_step")

    return {"foo": "bar"}


def main():

    system(
        "dotflow start --step docs_src.cli.cli_with_initial_context.simple_step "
        "--initial-context abc"
    )


if __name__ == "__main__":
    main()
