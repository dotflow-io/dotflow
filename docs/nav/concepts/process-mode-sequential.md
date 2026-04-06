# Sequential

Tasks run one after another. Each task receives the output of the previous one as `previous_context`.

## Implementation

{* ./docs_src/process_mode/sequential.py hl[26] *}

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
