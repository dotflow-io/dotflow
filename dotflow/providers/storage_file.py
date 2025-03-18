"""Storage File"""

from pathlib import Path
from typing import Any, Callable
from json import dumps, loads

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.utils import read_file, write_file
from dotflow.settings import Settings as settings


class StorageFile(Storage):
    """Storage"""

    def __init__(self, *args, path: str = settings.START_PATH, **kwargs):
        self.path = Path(path, "tasks")
        self.path.mkdir(parents=True, exist_ok=True)

    def post(self, key: str, context: Context) -> None:
        task_context = []

        if Path(self.path, key).exists():
            task_context = read_file(path=Path(self.path, key))

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))

            write_file(path=Path(self.path, key), content=task_context, mode="a")
            return None

        task_context.append(self._dumps(storage=context.storage))
        write_file(path=Path(self.path, key), content=task_context)
        return None

    def get(self, key: str) -> Context:
        task_context = []

        if Path(self.path, key).exists():
            task_context = read_file(path=Path(self.path, key))

        if len(task_context) == 1:
            return self._loads(storage=task_context[0])

        contexts = Context(storage=[])
        for context in task_context:
            contexts.storage.append(self._loads(storage=context))

        return contexts

    def key(self, task: Callable):
        return f"{task.workflow_id}-{task.task_id}.json"

    def _loads(self, storage: Any) -> Context:
        try:
            return Context(storage=loads(storage))
        except Exception:
            return Context(storage=storage)

    def _dumps(self, storage: Any) -> str:
        try:
            return dumps(storage)
        except TypeError:
            return str(storage)
