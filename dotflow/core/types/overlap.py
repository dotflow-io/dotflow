"""Type Overlap mode module"""

from typing import Annotated

from typing_extensions import Doc


class TypeOverlap:
    """
    Import:
        You can import the **TypeOverlap** class with:

            from dotflow.core.types import TypeOverlap
    """

    SKIP: Annotated[str, Doc("Skip if previous run is still active.")] = "skip"
    QUEUE: Annotated[
        str, Doc("Queue execution, run when previous completes.")
    ] = "queue"
    PARALLEL: Annotated[
        str, Doc("Run regardless, even if previous is still active.")
    ] = "parallel"
