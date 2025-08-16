from dotflow import DotFlow, action


def my_callback(*args, **kwargs):
    print(args, kwargs)


@action
def my_task():
    print("task")


workflow = DotFlow()
workflow.task.add(step=my_task, callback=my_callback)
workflow.start()
