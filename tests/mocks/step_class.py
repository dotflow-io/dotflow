"""Mock Class"""

import logging

from dotflow.core.action import Action as action


@action
class ActionStep:

    @action
    def run() -> None:
        logging.info("ActionStep: Run function executed")
        return {"foo": "bar"}


@action
class ActionStepExecutionOrderer:

    @action
    def func_f() -> None:
        return True

    @action
    def func_e() -> None:
        return True

    @action
    def func_d() -> None:
        return True

    @action
    def func_c() -> None:
        return True

    @action
    def func_b() -> None:
        return True

    @action
    def func_a() -> None:
        return True


@action
class ActionStepWithInitialContext:

    @action
    def run(initial_context) -> None:
        logging.debug("Run function executed")
        assert initial_context.storage
        return {"foo": "bar"}


@action
class ActionStepWithPreviousContext:

    @action
    def run_x(previous_context) -> None:
        assert previous_context.storage, {"context": True}
        return {"func": "run_x"}

    @action
    def run_y(previous_context) -> None:
        assert previous_context.storage, {"func": "run_x"}
        return {"func": "run_y"}


@action
class ActionStepWithContexts:

    @action
    def run(initial_context, previous_context) -> None:
        assert initial_context.storage, {"context": True}
        assert previous_context.storage, {"context": True}
        return {"foo": "bar"}


@action
class ActionStepWithError:

    @action
    def run() -> None:
        logging.debug("ActionStepWithError: Run function executed")
        raise Exception("Fail!")


@action
class ActionStepWithoutInit:

    @action
    def run() -> None:
        return {"foo": "bar"}


class SimpleStep:

    def run() -> None:
        return {"foo": "bar"}
