"""Module Mock"""

import logging

from dotflow.core.action import Action as action


@action
def action_step() -> None:
    pass


def simple_step() -> None:
    pass


def simple_callback(*args, **kwargs):
    pass


def dummy_step_with_fail() -> None:
    logging.error("Fail!")
    raise Exception("Fail!")


def dummy_step_previous_context(previous_context):
    logging.debug(previous_context.storage)
