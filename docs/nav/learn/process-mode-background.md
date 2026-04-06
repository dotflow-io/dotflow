# Background

Tasks run sequentially in a background thread, freeing the main thread for other work.

## Implementation

{* ./docs_src/process_mode/background.py hl[26] *}

## Workflow

```mermaid
flowchart TD
A[Start] -->|run| B
B[task_foo] -->|response to| C
C[task_bar] -->|response| D
D[Finish]
```

## References

- [Manager](https://dotflow-io.github.io/dotflow/nav/reference/workflow/)
