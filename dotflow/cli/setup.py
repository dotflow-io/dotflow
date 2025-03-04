"""Setup module"""

from rich import print  # type: ignore

from dotflow import __version__, __description__
from dotflow.log import logger
from dotflow.settings import Settings as settings
from dotflow.core.utils.basic_functions import basic_callback
from dotflow.core.models.execution import TypeExecution
from dotflow.core.exception import (
    MissingActionDecorator,
    ExecutionModeNotExist,
    StepMissingInit,
    ModuleNotFound,
    MESSAGE_UNKNOWN_ERROR,
)
from dotflow.cli.commands import InitCommand, ServerCommand, StartCommand


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
            help="Show program's version number and exit.",
        )

        self.setup_init()
        self.setup_start()
        self.command()

    def setup_server(self):
        self.cmd_server = self.subparsers.add_parser("server", help="Server")
        self.cmd_server = self.cmd_server.add_argument_group(
            "Usage: dotflow server [OPTIONS]"
        )
        self.cmd_server.set_defaults(exec=ServerCommand)

    def setup_init(self):
        self.cmd_init = self.subparsers.add_parser("init", help="Init")
        self.cmd_init = self.cmd_init.add_argument_group(
            "Usage: dotflow init [OPTIONS]"
        )
        self.cmd_init.set_defaults(exec=InitCommand)

    def setup_start(self):
        self.cmd_start = self.subparsers.add_parser("start", help="Start")
        self.cmd_start = self.cmd_start.add_argument_group(
            "Usage: dotflow start [OPTIONS]"
        )

        self.cmd_start.add_argument("-s", "--step", required=True)
        self.cmd_start.add_argument("-c", "--callback", default=basic_callback)
        self.cmd_start.add_argument("-i", "--initial-context")
        self.cmd_start.add_argument(
            "-o", "--output-context", default=False, action="store_true"
        )
        self.cmd_start.add_argument("-p", "--path", default=settings.INITIAL_PATH)
        self.cmd_start.add_argument(
            "-m",
            "--mode",
            default=TypeExecution.SEQUENTIAL,
            choices=[TypeExecution.SEQUENTIAL, TypeExecution.BACKGROUND],
        )

        self.cmd_start.set_defaults(exec=StartCommand)

    def command(self):
        message_icon = ":game_die:"
        message_error = "[bold red]Error:[/bold red]"
    
        try:
            arguments = self.parser.parse_args()
            if hasattr(arguments, "exec"):
                arguments.exec(parser=self.parser, arguments=arguments)
            else:
                print(__description__)
        except MissingActionDecorator as err:
            print(message_icon, message_error, err)

        except ExecutionModeNotExist as err:
            print(message_icon, message_error, err)

        except StepMissingInit as err:
            print(message_icon, message_error, err)

        except ModuleNotFound as err:
            print(message_icon, message_error, err)

        except Exception as err:
            print(message_icon, message_error, MESSAGE_UNKNOWN_ERROR)
            logger.error(err)
