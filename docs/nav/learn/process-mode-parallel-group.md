# Parallel Group

Tasks are organized into named groups. Groups run in parallel, but tasks within each group run sequentially, passing context between them.

## Implementation

{* ./docs_src/process_mode/parallel_group.py hl[26] *}

## Workflow

```mermaid
flowchart TD
    A[Start] -->|run| C(Parallel Groups)
    C -->|run| D[task_a]
    C -->|run| E[task_c]
    D -->|response| X[task_b]
    X --> H[Finish]
    E -->|response| Y[task_d]
    Y --> H[Finish]
```

## References

- [Task Groups](https://dotflow-io.github.io/dotflow/nav/tutorial/groups/)
- [Manager](https://dotflow-io.github.io/dotflow/nav/reference/workflow/)
