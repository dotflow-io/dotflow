"""Storage File"""

from collections.abc import Callable
from json import dumps, loads
from pathlib import Path
from typing import Any

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.settings import Settings as settings
from dotflow.utils import read_file, write_file


class StorageFile(Storage):
    """Storage"""

    def __init__(self, *args, path: str = settings.START_PATH, **kwargs):
        self.path = Path(path, "tasks")
        self.path.mkdir(parents=True, exist_ok=True)

    def post(self, key: str, context: Context) -> None:
        task_context = []

        if Path(self.path, key).exists():
            data = read_file(path=Path(self.path, key))
            if isinstance(data, list):
                task_context = data

        if isinstance(context.storage, list):
            for item in context.storage:
                if isinstance(item, Context):
                    task_context.append(self._dumps(storage=item.storage))
        else:
            task_context.append(self._dumps(storage=context.storage))

        write_file(path=Path(self.path, key), content=task_context)
        return None

    def get(self, key: str) -> Context:
        task_context = []

        if Path(self.path, key).exists():
            data = read_file(path=Path(self.path, key))
            if isinstance(data, list):
                task_context = data

        if not task_context:
            return Context()

        if len(task_context) == 1:
            return self._loads(storage=task_context[0])

        contexts = Context(storage=[])
        for context in task_context:
            contexts.storage.append(self._loads(storage=context))

        return contexts

    def key(self, task: Callable):
        return f"{task.workflow_id}-{task.task_id}.json"

    def clear(self, workflow_id: str) -> None:
        prefix = f"{workflow_id}-"

        for entry in self.path.iterdir():
            if entry.is_file() and entry.name.startswith(prefix):
                entry.unlink(missing_ok=True)

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
