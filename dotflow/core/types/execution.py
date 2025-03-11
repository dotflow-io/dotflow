"""Type Execution mode module"""

from typing_extensions import Annotated, Doc


class TypeExecution:
    """
    Import:
        You can import the **TypeExecution** class with:

            from dotflow.core.types import TypeExecution
    """

    SEQUENTIAL: Annotated[str, Doc("Sequential execution.")] = "sequential"
    BACKGROUND:  Annotated[str, Doc("Background execution.")] = "background"
    PARALLEL:  Annotated[str, Doc("Parallel execution.")] = "parallel"
    DATA_STORE:  Annotated[str, Doc("Data store execution.")] = "data_store"
