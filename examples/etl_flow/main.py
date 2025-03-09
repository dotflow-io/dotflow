#!/usr/bin/env python

from dotflow import DotFlow

from examples.etl_flow.tasks.extract import extract
from examples.etl_flow.tasks.transform import Transform
from examples.etl_flow.tasks.load import load


def main():
    url = "https://pythonfluente.com"
    workflow = DotFlow()

    workflow.task.add(step=extract, initial_context=url)
    workflow.task.add(step=Transform)
    workflow.task.add(step=load)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
