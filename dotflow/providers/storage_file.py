"""Local"""

from pathlib import Path
from typing import Callable

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.utils import read_file, write_file
from dotflow.settings import Settings as settings


class StorageFile(Storage):
    """Storage"""

    def __init__(self, path: str = settings.START_PATH, *args, **kwargs):
        self.path = Path(path, "tasks")
        self.path.mkdir(parents=True, exist_ok=True)

    def post(self, key: str, context: Context) -> None:
        if isinstance(context.storage, list):
            content = ""
            for item in context.storage:
                if isinstance(item, Context):
                    content += f"{str(item.storage)}\n"

            write_file(path=Path(self.path, key), content=content, mode="a")
            return None

        write_file(path=Path(self.path, key), content=str(context.storage))

    def get(self, key: str) -> Context:
        return Context(storage=read_file(path=Path(self.path, key)))

    def key(self, task: Callable):
        return f"{task.workflow_id}-{task.task_id}"
