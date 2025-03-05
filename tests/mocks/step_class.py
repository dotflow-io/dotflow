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
class ActionStepWithInitialContext:

    def __init__(self):
        pass

    @action
    def run(initial_context) -> None:
        assert initial_context.storage
        return {"foo": "bar"}


@action
class ActionStepWithPreviousContext:

    def __init__(self):
        pass

    @action
    def run(previous_context) -> None:
        assert previous_context.storage
        return {"foo": "bar"}


@action
class ActionStepWithContexts:

    def __init__(self):
        pass

    @action
    def run(initial_context, previous_context) -> None:
        assert initial_context.storage
        assert previous_context.storage
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
