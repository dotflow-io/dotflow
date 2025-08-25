"""Print"""

from rich import print


ICON = ":game_die:"


def print_error(value):
    print(f"{ICON} [bold red]Error:[/bold red]", value)


def print_info(value):
    print(f"{ICON} [bold blue]Info:[/bold blue]", value)


def print_warning(value):
    print(f"{ICON} [bold yellow]Warning:[/bold yellow]", value)
