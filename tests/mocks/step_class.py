"""Step Class"""

from dotflow.core.action import Action as action


@action
class ActionStep:

    def __init__(self):
        pass

    @action
    def run() -> None:
        return {"foo": "bar"}


@action
class ActionStepWithError:

    def __init__(self):
        pass

    @action
    def run() -> None:
        raise Exception("Fail!")


@action
class ActionStepWithoutInit:

    @action
    def run() -> None:
        return {"foo": "bar"}


class SimpleStep:

    def run() -> None:
        return {"foo": "bar"}
