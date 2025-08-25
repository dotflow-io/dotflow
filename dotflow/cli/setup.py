"""Setup module"""

from pathlib import Path

from dotflow import __version__, __description__
from dotflow.providers.otel.logs import client
from dotflow.utils.basic_functions import basic_callback
from dotflow.core.types import ExecutionModeType, StorageType
from dotflow.core.exception import (
    MissingActionDecorator,
    ExecutionModeNotExist,
    ImportModuleError,
    MESSAGE_UNKNOWN_ERROR,
)
from dotflow.cli.commands import InitCommand, StartCommand
from dotflow.utils.print import print_error, print_warning


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
            "-o", "--storage", choices=[StorageType.DEFAULT, StorageType.FILE]
        )
        self.cmd_start.add_argument("-p", "--path", default=Path())
        self.cmd_start.add_argument(
            "-m",
            "--mode",
            default=ExecutionModeType.SEQUENTIAL,
            choices=[
                ExecutionModeType.SEQUENTIAL,
                ExecutionModeType.BACKGROUND,
                ExecutionModeType.PARALLEL,
            ],
        )

        self.cmd_start.set_defaults(exec=StartCommand)

    def command(self):
        try:
            arguments = self.parser.parse_args()
            if hasattr(arguments, "exec"):
                arguments.exec(parser=self.parser, arguments=arguments)
            else:
                print(__description__)
        except MissingActionDecorator as err:
            print_warning(err)

        except ExecutionModeNotExist as err:
            print_warning(err)

        except ImportModuleError as err:
            print_warning(err)

        except Exception as err:
            client.error(f"Internal problem: {str(err)}")
            print_error(MESSAGE_UNKNOWN_ERROR)
