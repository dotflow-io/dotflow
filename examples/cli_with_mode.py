#!/usr/bin/env python

from time import sleep
from os import system

from dotflow import action


@action
def simple_step():
    sleep(3)
    return "ok"


def main():
    """Output
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - Not started
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - In progress
    0000-00-00 00:00:00,000 - INFO [dotflow]: ID 56a908c5-c9f2-4ebf-a00a-895e49bd189b - 0 - Completed
    """
    system("dotflow start --step examples.cli_with_mode.simple_step --mode sequential")
    system("dotflow start --step examples.cli_with_mode.simple_step --mode background")


if __name__ == "__main__":
    main()
