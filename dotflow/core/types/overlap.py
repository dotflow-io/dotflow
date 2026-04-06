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
        str,
        Doc(
            "Queue at most one pending execution. "
            "When the current run completes, the queued run starts. "
            "Extra triggers while a run is queued are dropped."
        ),
    ] = "queue"
    PARALLEL: Annotated[
        str,
        Doc(
            "Run concurrently, up to 10 simultaneous executions. "
            "Extra triggers beyond the limit are dropped."
        ),
    ] = "parallel"
