"""Type Execution mode module"""

from typing import Annotated

from typing_extensions import Doc


class TypeExecution:
    """
    Import:
        You can import the **TypeExecution** class with:

            from dotflow.core.types import TypeExecution
    """

    SEQUENTIAL: Annotated[str, Doc("Sequential execution.")] = "sequential"
    BACKGROUND: Annotated[str, Doc("Background execution.")] = "background"
    PARALLEL: Annotated[str, Doc("Parallel execution.")] = "parallel"
