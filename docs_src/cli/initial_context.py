import json

from os import system

from dotflow import action


@action
def simple_step(initial_context):
    assert json.loads(initial_context.storage) == {"foo": "bar"}

    return initial_context


def main():
    """
    COMMAND:
        dotflow start --step docs_src.cli.initial_context.simple_step --initial-context "{'foo': 'bar'}"

    OUTPUT:
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - In queue
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - In progress
        0000-00-00 00:00:00,000 - INFO [dotflow]: 0: 1c88c8d5-a456-46e6-98b9-ceee3d223c88 - Success
    """

    system("""dotflow start --step docs_src.cli.initial_context.simple_step --initial-context '{"foo": "bar"}'""")


if __name__ == "__main__":
    main()
