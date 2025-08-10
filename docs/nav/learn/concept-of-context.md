# Concept of Context

When referring to **[Context](https://dotflow-io.github.io/dotflow/nav/reference/context/)** within the Dotflow library, we are talking about how data is transferred within tasks. The **[Context](https://dotflow-io.github.io/dotflow/nav/reference/context/)** is essentially a class embedded in every task return. This class is standardized, and you can access its value through the `storage` object.

/// note

The **[Context](https://dotflow-io.github.io/dotflow/nav/reference/context/)** class pattern is applied to the **Initial Context** and the **Previous Context** of a task.

///

## Accessing context data

{* ./docs_src/context/context.py hl[10] *}

For implementation details of the class, you can access them [here](https://dotflow-io.github.io/dotflow/nav/reference/context/ "Context class")