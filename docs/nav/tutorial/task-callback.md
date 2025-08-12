# Task

Tasks can also receive a specific callback, and it’s quite simple.

## Receiving callback

In this example, we receive a [Task](https://dotflow-io.github.io/dotflow/pt/nav/reference/task/ "Task class") object.

{* ./docs_src/callback/task_callback.py ln[5:12] hl[5,10] *}

## Including callback in the tasks

To add a callback to a task, simply include it when adding the task to the queue — and that’s it, the callback will be executed once the task finishes.

{* ./docs_src/callback/task_callback.py ln[25:32] hl[28:29] *}

/// warning

The parameter `keep_going` was included to keep the workflow running even if a task fails.

///

{* ./docs_src/callback/task_callback.py ln[25:32] hl[30] *}
