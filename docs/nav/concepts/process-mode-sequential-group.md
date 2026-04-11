# Sequential Group

Tasks are organized into named groups. Groups run sequentially one after another, and tasks within each group also run sequentially, passing context between them.

This mode is automatically selected when you use `mode="sequential"` with multiple groups. You can also use `mode="sequential_group"` explicitly.

## Implementation

```python
from dotflow import DotFlow, action


@action
def step_a():
    return {"group": "A", "step": 1}


@action
def step_b(previous_context):
    return {"group": "A", "step": 2}


@action
def step_c():
    return {"group": "B", "step": 1}


@action
def step_d(previous_context):
    return {"group": "B", "step": 2}


workflow = DotFlow()
workflow.task.add(step=step_a, group_name="group_a")
workflow.task.add(step=step_b, group_name="group_a")
workflow.task.add(step=step_c, group_name="group_b")
workflow.task.add(step=step_d, group_name="group_b")

workflow.start(mode="sequential_group")
```

## Workflow

```mermaid
flowchart TD
    A[Start] -->|run| B[Group A]
    B --> C[step_a]
    C -->|response| D[step_b]
    D --> E[Group B]
    E --> F[step_c]
    F -->|response| G[step_d]
    G --> H[Finish]
```

## References

- [Task Groups](https://dotflow-io.github.io/dotflow/nav/tutorial/groups/)
- [Manager](https://dotflow-io.github.io/dotflow/nav/reference/workflow/)
