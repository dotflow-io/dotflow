"""Command module"""


class Command:

    def __init__(self, **kwargs):
        self.params = kwargs.get("arguments")

        if hasattr(self.params, "option"):
            getattr(self, self.params.option)()
