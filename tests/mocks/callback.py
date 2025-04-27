"""Callback Mock"""

from logging import error


def simple_callback(*args, **kwargs):
    error(kwargs.get("task").task_id)
