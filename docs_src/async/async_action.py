import asyncio

from dotflow import DotFlow, action


@action
async def fetch_users():
    await asyncio.sleep(0.1)
    return {"users": ["Alice", "Bob"]}


@action
async def fetch_orders():
    await asyncio.sleep(0.1)
    return {"orders": [1, 2, 3]}


@action
def process(previous_context):
    return {"processed": previous_context.storage}


def main():
    workflow = DotFlow()

    workflow.task.add(step=fetch_users)
    workflow.task.add(step=process)
    workflow.start()

    for task in workflow.result_task():
        print(f"Task {task.task_id}: {task.status}")

    return workflow


if __name__ == "__main__":
    main()
