"""Error handler module"""

import traceback


def traceback_error(error: Exception) -> str:
    return "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    ).rstrip()


def message_error(error: Exception) -> str:
    return str(error)
