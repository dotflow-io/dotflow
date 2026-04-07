"""Command module"""

from abc import ABC, abstractmethod


class Command(ABC):

    def __init__(self, **kwargs):
        self.params = kwargs.get("arguments")
        self.setup()

    @abstractmethod
    def setup(self):
        pass
