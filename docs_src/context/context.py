from dotflow import Context

new_context = Context(
    storage={"data": [0, 1, 2, 3]}
)

print(new_context.time)
print(new_context.task_id)
print(new_context.workflow_id)
print(new_context.storage)
