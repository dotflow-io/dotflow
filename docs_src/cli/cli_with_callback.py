from os import system

from dotflow import action


def callback(*args, **kwargs):
    print(args, kwargs)


@action
def simple_step():
    return "ok"


def main():
    system(
        "dotflow start --step docs_src.cli.cli_with_callback:simple_step "
        "--callback docs_src.cli.cli_with_callback:callback"
    )


if __name__ == "__main__":
    main()
