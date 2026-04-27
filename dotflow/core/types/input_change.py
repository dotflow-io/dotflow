"""Type InputChange policy module."""

from typing import Annotated

from typing_extensions import Doc


class TypeInputChange:
    """
    Import:
        You can import the **TypeInputChange** class with:

            from dotflow.core.types import TypeInputChange
    """

    REUSE: Annotated[
        str, Doc("Keep prior checkpoints; ignore the new input.")
    ] = "reuse"
    RESET: Annotated[str, Doc("Drop prior checkpoints and start fresh.")] = (
        "reset"
    )
    RAISE: Annotated[str, Doc("Refuse to start; raise InputChangedError.")] = (
        "raise"
    )


VALID_POLICIES = (
    TypeInputChange.REUSE,
    TypeInputChange.RESET,
    TypeInputChange.RAISE,
)
