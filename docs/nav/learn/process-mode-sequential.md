# Sequential

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
