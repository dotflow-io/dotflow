"""Utils module"""

from typing import Any

from dotflow.core.context import Context


def store_context(content: Any):
    if not isinstance(content, Context):
        return Context(storage=content)
    return content
