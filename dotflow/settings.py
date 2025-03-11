"""Settings"""

from pathlib import Path


class Settings:
    """Settings DotFlow"""

    START_PATH = Path(".output")
    GITIGNORE = Path(".gitignore")

    LOG_PROFILE = "dotflow"
    LOG_FILE_NAME = Path("flow.log")
    LOG_PATH = Path(".output/flow.log")
    LOG_FORMAT = "%(asctime)s - %(levelname)s [%(name)s]: %(message)s"

    ICON = ":game_die:"
    ERROR_ALERT = f"{ICON} [bold red]Error:[/bold red]"
    INFO_ALERT = f"{ICON} [bold blue]Info:[/bold blue]"
    WARNING_ALERT = f"{ICON} [bold yellow]Warning:[/bold yellow]"
