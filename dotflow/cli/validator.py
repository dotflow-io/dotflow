"""Validator module"""

from argparse import Namespace


class Validator:

    def __init__(self, params: Namespace):
        self.attr = {}
        self.params = params

        for func in dir(self):
            if func.startswith("input_"):
                field = func.replace("input_", "")

                if hasattr(params, field):
                    self.attr[field] = getattr(self, func)(getattr(params, field))
