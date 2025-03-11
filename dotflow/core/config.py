"""Config module"""

from pathlib import Path

from dotflow.settings import Settings as settings


class Config:
    """
    Import:
        You can import the **Config** class with:

            from dotflow.core.config import Config

    Example:
        `class` dotflow.core.config.Config

            config = Config(
                path=".output",
                output=False
            )

    Args:
        path (str): Initial path of the library.
        output (bool): Flag for storing context in a file.

    Attributes:
        path (Path):
        task_path (Path):
        log_path (Path):
        output (str):
    """

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
