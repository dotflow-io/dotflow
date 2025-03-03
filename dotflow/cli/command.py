"""Command module"""

from dotflow.cli.storage import Storage


class Command:

    def __init__(self, **kwargs):
        self.storage = Storage()
        self.params = kwargs.get("arguments")

        if hasattr(self.params, "option"):
            getattr(self, self.params.option)()
