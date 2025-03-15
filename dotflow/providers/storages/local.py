"""Local"""

from pathlib import Path

from dotflow.abc.storage import Storage
from dotflow.core.context import Context
from dotflow.utils import read_file, write_file
from dotflow.settings import Settings as settings


class StorageLocal(Storage):
    """Storage"""

    def __init__(self, path: str = settings.START_PATH):
        self.path = Path(path, "tasks")
        self.path.mkdir(parents=True, exist_ok=True)

    def post(self, key: str, context: Context) -> None:
        """Post context"""
        write_file(
            path=Path(self.path, key),
            content=context.storage
        )

    def get(self, key: str) -> Context:
        """Get context"""
        return Context(
            storage=read_file(
                path=Path(self.path, key)
            )
        )
