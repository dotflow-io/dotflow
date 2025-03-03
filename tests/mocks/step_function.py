"""Step Function"""

import logging

from dotflow.core.action import Action as action


@action
def action_step() -> None:
    return {"foo": "bar"}


@action(retry=1)
def action_step_with_retry() -> None:
    return {"foo": "bar"}


@action
def action_step_with_error() -> None:
    raise Exception("Fail!")


def simple_step() -> None:
    return {"foo": "bar"}


def simple_step_with_params(foo, bar) -> None:
    return {"foo": "bar"}


def simple_step_with_fail() -> None:
    logging.error("Fail!")
    raise Exception("Fail!")


def simple_step_with_initial_context(initial_context):
    logging.debug(initial_context.storage)


def simple_step_with_previous_context(previous_context):
    logging.debug(previous_context.storage)
