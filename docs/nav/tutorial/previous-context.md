# Previous Context

## Sending context

To send a context, just return some information in your task implementation. You can return any object, and it will become part of the context.

{* ./docs_src/previous_context/previous_context.py hl[15,23] *}


## Receiving context

In this example, an previous context value is received from the `previous_contexto` attribute defined in the function.

{* ./docs_src/previous_context/previous_context.py hl[11,19] *}