"""Time module"""

from datetime import datetime


def time(func):
    """"Time Decorator"""
    def inside(*args, **kwargs):
        start = datetime.now()
        task = func(*args, **kwargs)
        task.duration = (datetime.now() - start).total_seconds()
        return task
    return inside
