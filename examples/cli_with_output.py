#!/usr/bin/env python

from os import system

from dotflow import action


@action
def simple_step():
    return {"foo": "bar"}


def main():
    """
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Initial Context -> None
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Not started
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - In progress
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Completed
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 5ace2ca5-3d88-4119-a064-a9ae048826e9 - 0 - Current Context -> {'foo': 'bar'}
    """
    system("dotflow start --step examples.cli_with_output.simple_step --output")


if __name__ == "__main__":
    main()
