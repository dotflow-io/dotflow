# Workflow

The callback mechanism in a Workflow is global, meaning that it applies to all tasks added to the execution queue. There are two types of workflow callbacks:

## Success Callback

This callback is triggered only when the entire workflow completes successfully, with all tasks executed without errors.

### Including callback on success

{* ./docs_src/callback/workflow_callback_success.py ln[19:25] hl[23] *}

### Receiving callback

{* ./docs_src/callback/workflow_callback_success.py ln[5:11] hl[5] *}


## Failure Callback

This callback is triggered if any task in the workflow fails during execution.

These callbacks should be used to handle post-execution actions depending on the overall result of the workflow, such as logging, notifications, or cleanup operations.

### Including callback on failure

{* ./docs_src/callback/workflow_callback_failure.py ln[19:25] hl[23] *}

### Receiving callback

{* ./docs_src/callback/workflow_callback_failure.py ln[5:11] hl[5] *}
