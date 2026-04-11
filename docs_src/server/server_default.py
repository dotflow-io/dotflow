from dotflow import Config, DotFlow, action
from dotflow.providers import ServerDefault


@action
def extract():
    return {"users": 150}


@action
def transform(previous_context):
    total = previous_context.storage["users"]
    return {"users": total, "active": int(total * 0.8)}


@action
def load(previous_context):
    return (
        f"Loaded {previous_context.storage['active']}"
        " active users"
    )


def main():
    config = Config(
        server=ServerDefault(
            base_url="http://localhost:8000/api/v1",
            user_token="your-api-token",
        )
    )

    workflow = DotFlow(config=config)
    workflow.task.add(step=extract)
    workflow.task.add(step=transform)
    workflow.task.add(step=load)

    workflow.start()

    return workflow


if __name__ == "__main__":
    main()
