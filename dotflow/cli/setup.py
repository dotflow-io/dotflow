"""Setup module"""

from rich import print  # type: ignore

from dotflow import __version__, __description__
from dotflow.log import logger
from dotflow.config import Config
from dotflow.core.utils.basic_functions import basic_callback
from dotflow.core.exception import (
    MissingActionDecorator,
    ExecutionModeNotExist,
    StepMissingInit,
    ModuleNotFound,
    MESSAGE_UNKNOWN_ERROR
)
from dotflow.cli.commands import (
    ServerCommand,
    StartCommand
)


class Command:

    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers()
        self.parser._positionals.title = "Commands"
        self.parser._optionals.title = "Default Options"
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"dotflow=={__version__}",
            help="Show program's version number and exit."
        )

        self.setup_start()
        self.command()

    def setup_server(self):
        self.cmd_server = self.subparsers.add_parser("server", help="Server")
        self.cmd_server = self.cmd_server.add_argument_group("Usage: dotflow server [OPTIONS]")
        self.cmd_server.set_defaults(exec=ServerCommand)

    def setup_start(self):
        self.cmd_start = self.subparsers.add_parser("start", help="Task")
        self.cmd_start = self.cmd_start.add_argument_group("Usage: dotflow task [OPTIONS]")

        self.cmd_start.add_argument("-s", "--step", required=True)
        self.cmd_start.add_argument("-c", "--callback", default=basic_callback)
        self.cmd_start.add_argument("-i", "--initial-context")
        self.cmd_start.add_argument("-o", "--output", default=False, action='store_true')
        self.cmd_start.add_argument("-p", "--path", default=Config.PATH)

        self.cmd_start.set_defaults(exec=StartCommand)

    def command(self):
        try:
            arguments = self.parser.parse_args()
            if hasattr(arguments, "exec"):
                arguments.exec(parser=self.parser, arguments=arguments)
            else:
                print(__description__)
        except MissingActionDecorator as err:
            print(":game_die:", "[bold red]Error:[/bold red]", err)

        except ExecutionModeNotExist as err:
            print(":game_die:", "[bold red]Error:[/bold red]", err)

        except StepMissingInit as err:
            print(":game_die:", "[bold red]Error:[/bold red]", err)

        except ModuleNotFound as err:
            print(":game_die:", "[bold red]Error:[/bold red]", err)

        except Exception as err:
            print(":game_die:", "[bold red]Error:[/bold red]", MESSAGE_UNKNOWN_ERROR)
            logger.error(err)
