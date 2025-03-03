#!/usr/bin/env python

from os import system

from dotflow import action


def callback(*args, **kwargs):
    print(args, **kwargs)


@action
def simple_step():
    return "ok"


if __name__ == "__main__":
    system("dotflow task start --step examples.cli.simple_step")
