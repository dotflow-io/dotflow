"""Setup module"""

from rich import print  # type: ignore

from dotflow import __version__, __description__
from dotflow.logging import logger
from dotflow.settings import Settings as settings
from dotflow.utils.basic_functions import basic_callback
from dotflow.core.types.execution import TypeExecution
from dotflow.core.exception import (
    MissingActionDecorator,
    ExecutionModeNotExist,
    ImportModuleError,
    MESSAGE_UNKNOWN_ERROR,
)
from dotflow.cli.commands import (
    InitCommand,
    LogCommand,
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
            help="Show program's version number and exit.",
        )

        self.setup_init()
        self.setup_logs()
        self.setup_start()
        self.command()

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
        self.cmd_start.add_argument("-o", "--storage", choices=["default", "file"])
        self.cmd_start.add_argument("-p", "--path", default=settings.START_PATH)
        self.cmd_start.add_argument(
            "-m",
            "--mode",
            default=TypeExecution.SEQUENTIAL,
            choices=[TypeExecution.SEQUENTIAL, TypeExecution.BACKGROUND],
        )

        self.cmd_start.set_defaults(exec=StartCommand)

    def setup_logs(self):
        self.cmd_logs = self.subparsers.add_parser("logs", help="Logs")
        self.cmd_logs = self.cmd_logs.add_argument_group("Usage: dotflow log [OPTIONS]")
        self.cmd_logs.set_defaults(exec=LogCommand)

    def command(self):
        try:
            arguments = self.parser.parse_args()
            if hasattr(arguments, "exec"):
                arguments.exec(parser=self.parser, arguments=arguments)
            else:
                print(__description__)
        except MissingActionDecorator as err:
            print(settings.WARNING_ALERT, err)

        except ExecutionModeNotExist as err:
            print(settings.WARNING_ALERT, err)

        except ImportModuleError as err:
            print(settings.WARNING_ALERT, err)

        except Exception as err:
            logger.error(f"Internal problem: {str(err)}")
            print(settings.ERROR_ALERT, MESSAGE_UNKNOWN_ERROR)
