# Workflow and tasks

A **workflow** in Dotflow is an ordered set of **tasks** built on a [`DotFlow`](../reference/dotflow.md) instance. You register steps with `workflow.task.add(...)`, then run them through **`start`** (one-shot execution) or **`schedule`** (recurring runs when a scheduler is configured).

## Main pieces

| Piece | Role |
|-------|------|
| [`DotFlow`](../reference/dotflow.md) | Entry point: holds `config`, `workflow_id`, and the task builder. |
| [`TaskBuilder`](../reference/task-builder.md) | Collects tasks in a queue before execution. |
| [`Manager`](../reference/workflow.md) | Runs the queue (sequential, background, or parallel) and coordinates storage and callbacks. |
| **Action** | A callable decorated with [`@action`](../reference/decorators.md); Dotflow wraps it as a unit of work with context in/out. |

Each task consumes **previous context** from the prior step and can emit a new **context** for the next one. See [Concept of context](concept-of-context.md) and the [Initial context](../tutorial/initial-context.md) / [Previous context](../tutorial/previous-context.md) how-tos.

## Execution vs scheduling

- **`start`** runs the workflow now (see [Process Mode](process-mode-sequential.md) for *how* tasks are ordered and parallelized).
- **`schedule`** delegates to the configured **scheduler** (for example cron); overlap between runs is controlled by [overlap strategies](concept-cron-overlap.md).

## References

- [`DotFlow`](../reference/dotflow.md)
- [`Task`](../reference/task.md)
- [First steps](../tutorial/first-steps.md)
