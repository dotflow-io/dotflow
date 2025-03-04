"""Config module"""

from dotflow.core.utils import make_dir
from dotflow.settings import Settings as settings


class Config:

    def __init__(
            self,
            path: str = settings.INITIAL_PATH,
            output: bool = False
    ) -> None:
        self.path = path
        self.log_path = f"{path}/{settings.LOG_FILE}"
        self.output = output

        make_dir(path=self.path, show_log=True)
