"""Mock Function"""

import logging
from typing import Any

from dotflow.core.action import Action as action


@action
def action_step() -> Any:
    return {"foo": "bar"}


@action
def action_step_with_initial_context(initial_context) -> Any:
    assert initial_context.storage
    return initial_context.storage


@action
def action_step_with_previous_context(previous_context) -> Any:
    assert previous_context.storage
    return previous_context.storage


@action
def action_step_with_contexts(initial_context, previous_context) -> Any:
    assert initial_context.storage
    assert previous_context.storage

    return initial_context, previous_context


@action(retry=1)
def action_step_with_retry() -> Any:
    return {"foo": "bar"}


@action
def action_step_with_error() -> Any:
    raise Exception("Fail!")


def simple_step() -> Any:
    return {"foo": "bar"}


def simple_step_with_params(foo, bar) -> Any:
    return {"foo": "bar"}


def simple_step_with_fail() -> Any:
    logging.error("Fail!")
    raise Exception("Fail!")


def simple_step_with_initial_context(initial_context) -> None:
    logging.debug(initial_context.storage)


def simple_step_with_previous_context(previous_context) -> None:
    logging.debug(previous_context.storage)
