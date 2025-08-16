# Parallel

{* ./docs_src/process_mode/parallel.py hl[26] *}

## Workflow

```mermaid
flowchart TD
    S[Start] -->|run| A[task_a]
    S[Start] -->|run| B[task_b]
    S[Start] -->|run| C[task_c]
    S[Start] -->|run| D[task_d]
    A --> H[Finish]
    B --> H[Finish]
    C --> H[Finish]
    D --> H[Finish]
```