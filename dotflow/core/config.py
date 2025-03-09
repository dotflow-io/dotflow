"""Config module"""

from pathlib import Path

from dotflow.settings import Settings as settings


class Config:

    def __init__(
            self,
            path: str = settings.START_PATH,
            output: bool = False
    ) -> None:
        self.path = Path(path)
        self.task_path = Path(path, "tasks")
        self.log_path = Path(path, settings.LOG_FILE_NAME)
        self.output = output

        self.path.mkdir(parents=True, exist_ok=True)
        self.task_path.mkdir(parents=True, exist_ok=True)
