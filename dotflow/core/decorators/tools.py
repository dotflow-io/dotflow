"""Tools"""

import threading

from typing import Callable

from datetime import datetime


def time(func):
    def inside(*args, **kwargs):
        start = datetime.now()
        task = func(*args, **kwargs)
        task.duration = (datetime.now() - start).total_seconds()
        return task
    return inside


def _threading(func: Callable):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(
            target=func, args=args,
            kwargs=kwargs
        )
        thread.start()

        return thread
    return wrapper
