from dotflow import DotFlow, action


@action(retry=5)
class Step:

    def auxiliary_function(self):
        """This function will not be executed, because
        it does not have an 'action' decorator.
        """

    @action
    def first_function(self):
        return {"foo": "bar"}

    @action
    def second_function(self):
        return True


def main():
    workflow = DotFlow()

    workflow.task.add(step=Step)
    workflow.start()

    for contexts in workflow.result_context():
        for context in contexts.storage:
            print(context.time, context.storage)
            assert context.storage

    return workflow


if __name__ == "__main__":
    main()
