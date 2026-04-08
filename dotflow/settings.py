"""Settings"""

import os
from pathlib import Path

_OUTPUT = Path(os.environ.get("DOTFLOW_OUTPUT_PATH", ".output"))


class Settings:
    """Settings DotFlow"""

    START_PATH = _OUTPUT
    GITIGNORE = Path(".gitignore")

    LOG_PROFILE = "dotflow"
    LOG_FILE_NAME = Path("flow.log")
    LOG_PATH = _OUTPUT / "flow.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s [%(name)s]: %(message)s"

    TEMPLATE_REPO = "https://github.com/dotflow-io/template.git"
    TEMPLATE_BRANCH = "master"
    TEMPLATE_CLOUD_DIR = "cloud"

    ICON = ":game_die:"
    ERROR_ALERT = f"{ICON} [bold red]Error:[/bold red]"
    INFO_ALERT = f"{ICON} [bold blue]Info:[/bold blue]"
    WARNING_ALERT = f"{ICON} [bold yellow]Warning:[/bold yellow]"
