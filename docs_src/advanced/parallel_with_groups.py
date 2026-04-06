from dotflow import DotFlow, action


@action
def fetch_users():
    return {"users": ["alice", "bob"]}


@action
def process_users(previous_context):
    return {"processed": len(previous_context.storage["users"])}


@action
def fetch_orders():
    return {"orders": [101, 102, 103]}


@action
def process_orders(previous_context):
    return {"total": len(previous_context.storage["orders"])}


def main():
    workflow = DotFlow()
    workflow.task.add(step=fetch_users, group_name="users")
    workflow.task.add(step=process_users, group_name="users")
    workflow.task.add(step=fetch_orders, group_name="orders")
    workflow.task.add(step=process_orders, group_name="orders")
    workflow.start(mode="sequential")


if __name__ == "__main__":
    main()
