"""Module Command"""

from dotflow import __version__, __description__
from dotflow.cli.commands.server import Server


class Command:

    def __init__(self, parser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers()
        self.parser._positionals.title = 'Commands'
        self.parser._optionals.title = 'Default Options'
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=f"dotflow=={__version__}",
            help="Show program's version number and exit."
        )

        self.setup_server()
        self.command()

    def setup_server(self):
        self.cmd_server = self.subparsers.add_parser('server', help="Server")
        self.cmd_server = self.cmd_server.add_argument_group('Usage: dotflow server [OPTIONS]')
        self.cmd_server.set_defaults(exec=Server)

    def command(self):
        arguments = self.parser.parse_args()
        if hasattr(arguments, 'exec'):
            arguments.exec(parser=self.parser, arguments=arguments)
        else:
            print(__description__)
