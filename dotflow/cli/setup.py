"""Setup module"""

from dotflow import __version__, __description__
from dotflow.core.utils.basic_functions import basic_callback
from dotflow.cli.commands import (
    ServerCommand,
    TaskCommand
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

        self.setup_task()
        self.command()

    def setup_server(self):
        self.cmd_server = self.subparsers.add_parser("server", help="Server")
        self.cmd_server = self.cmd_server.add_argument_group("Usage: dotflow server [OPTIONS]")
        self.cmd_server.set_defaults(exec=ServerCommand)

    def setup_task(self):
        self.cmd_task = self.subparsers.add_parser("task", help="Task")
        self.cmd_task = self.cmd_task.add_argument_group("Usage: dotflow task [OPTIONS]")
        self.cmd_task.add_argument("option", choices=["add", "start"])

        self.cmd_task.add_argument("-s", "--step", required=True)
        self.cmd_task.add_argument("-c", "--callback", default=basic_callback)
        self.cmd_task.add_argument("-i", "--initial-context")

        self.cmd_task.set_defaults(exec=TaskCommand)

    def command(self):
        arguments = self.parser.parse_args()
        if hasattr(arguments, "exec"):
            arguments.exec(parser=self.parser, arguments=arguments)
        else:
            print(__description__)
