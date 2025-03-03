"""Task validator module"""

from typing import Any
from dotflow.cli.validator import Validator


class TaskValidator(Validator):

    def input_step(self, value: Any):
        return value

    def input_callbback(self, value: Any):
        return value

    def input_initial_context(self, value: Any):
        return value
