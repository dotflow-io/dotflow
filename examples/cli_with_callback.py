#!/usr/bin/env python

from os import system

from dotflow import action


def callback(*args, **kwargs):
    print(args, kwargs)


@action
def simple_step():
    return "ok"


def main():
    """Output
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - Not started
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - In progress
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - Completed
    """
    system("dotflow start --step examples.cli_with_callback.simple_step --callback examples.cli_with_callback.callback")


if __name__ == "__main__":
    main()
