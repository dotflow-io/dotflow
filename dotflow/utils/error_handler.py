"""Error handler module"""

import sys
import traceback


def traceback_error(error: Exception) -> str:
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    message = "".join(exception_list)
    message = message[:-1]

    return message


def message_error(error: Exception) -> str:
    return str(error)
