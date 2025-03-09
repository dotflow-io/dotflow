from dotflow import action


@action
def load(previous_context):
    with open(file="book.json", mode="w", encoding="utf-8") as file:
        file.write(previous_context.storage[2].storage)
