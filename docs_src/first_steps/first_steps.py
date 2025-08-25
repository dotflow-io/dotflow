from dotflow import DotFlow, action, Task


def my_callback(task: Task):
    print(task.status)


@action
def my_task():
    print("task")


workflow = DotFlow()
workflow.add(step=my_task, callback=my_callback)
workflow.start()
