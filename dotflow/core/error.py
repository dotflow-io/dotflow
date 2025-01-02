"""Workflow"""


class IncorrectTypeContext(Exception):

    def __init__(self):
        message = "This object that was received is not of type Context."
        super(IncorrectTypeContext, self).__init__(message)
