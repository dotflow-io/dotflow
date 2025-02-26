"""Time module"""

from datetime import datetime


def time(func):
    def inside(*args, **kwargs):
        start = datetime.now()
        task = func(*args, **kwargs)
        task.set_duration((datetime.now() - start).total_seconds())
        return task
    return inside
