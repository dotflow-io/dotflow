#!/usr/bin/env python

from os import system

from dotflow import action


@action
def simple_step(initial_context):
    print(initial_context.storage, "simple_step")
    return {"foo": "bar"}


def main():
    """Output
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Not started
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - In progress
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Completed
    """
    system("dotflow start --step examples.cli_with_initial_context.simple_step --initial-context abc")


if __name__ == "__main__":
    main()
