#!/usr/bin/env python

import sys

from dotflow import DotFlow, Config
from dotflow.storage import StorageFile

from examples.etl_flow.tasks.extract import extract
from examples.etl_flow.tasks.transform import Transform
from examples.etl_flow.tasks.load import load


def main():
    url = "https://pythonfluente.com"

    workflow = DotFlow()

    if len(sys.argv) == 2 and sys.argv[1] == "file":
        config = Config(storage=StorageFile())
        workflow = DotFlow(config=config)

    workflow.task.add(step=extract, initial_context=url)
    workflow.task.add(step=Transform)
    workflow.task.add(step=load)
    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
