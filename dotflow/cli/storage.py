"""Storage module"""

import json

from os import makedirs, listdir


class Storage:

    PATHS = {
        "tasks": ".storage/tasks",
        "workflows": ".storage/workflows"
    }

    def __init__(self, **kwargs):
        for path in self.PATHS:
            makedirs(self.PATHS[path], exist_ok=True)

    def save_task(self, task: dict):
        task_id = self.next_task_id()
        file_path = f"{self.PATHS['tasks']}/{task_id}.json"

        with open(file=file_path, mode="w", encoding="utf-8") as file:
            file.write(json.dumps(task, indent=4))

    def list_tasks(self):
        return listdir(self.PATHS["tasks"])

    def list_workflows(self):
        return listdir(self.PATHS["workflows"])

    def next_task_id(self):
        return len(self.list_tasks()) + 1
