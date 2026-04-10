"""
Server provider with retry and backoff.

Task errors and retry_count are sent to the server
on each status change.
"""

from dotflow import Config, DotFlow, action
from dotflow.providers import ServerDefault


@action(retry=3, retry_delay=2, backoff=True)
def unreliable_task():
    import random

    if random.random() < 0.5:
        raise ValueError("Random failure")
    return {"result": "success"}


@action
def final_step(previous_context):
    print(f"Result: {previous_context.storage}")


def main():
    config = Config(
        server=ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="your-api-token",
        )
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=unreliable_task)
    workflow.task.add(step=final_step)

    workflow.start(keep_going=True)

    for task in workflow.result_task():
        print(
            f"Task {task.task_id}: "
            f"{task.status} "
            f"(retries: {task.retry_count})"
        )

    return workflow


if __name__ == "__main__":
    main()
