from os import system

from dotflow import action


@action
def simple_step():
    return "ok"


def main():
    system("dotflow start --step docs_src.basic.simple_cli.simple_step")


if __name__ == "__main__":
    main()
