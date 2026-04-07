"""Setup module"""

from rich import print  # type: ignore

from dotflow import __description__, __version__
from dotflow.cli.commands import (
    CloudGenerateCommand,
    CloudListCommand,
    InitCommand,
    LogCommand,
    ScheduleCommand,
    StartCommand,
)
from dotflow.core.exception import (
    MESSAGE_UNKNOWN_ERROR,
    ExecutionModeNotExist,
    ImportModuleError,
    MissingActionDecorator,
)
from dotflow.core.types import TypeExecution, TypeOverlap, TypeStorage
from dotflow.logging import logger
from dotflow.settings import Settings as settings
from dotflow.utils.basic_functions import basic_callback


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
        self.setup_schedule()
        self.setup_cloud()
        self.command()

    def setup_init(self):
        self.cmd_init = self.subparsers.add_parser(
            "init", help="Scaffold a new dotflow project"
        )
        self.cmd_init = self.cmd_init.add_argument_group(
            "Usage: dotflow init <project-name>"
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
            "-o",
            "--storage",
            choices=[
                TypeStorage.DEFAULT,
                TypeStorage.FILE,
                TypeStorage.S3,
                TypeStorage.GCS,
            ],
        )
        self.cmd_start.add_argument(
            "-p", "--path", default=settings.START_PATH
        )
        self.cmd_start.add_argument(
            "-m",
            "--mode",
            default=TypeExecution.SEQUENTIAL,
            choices=[
                TypeExecution.SEQUENTIAL,
                TypeExecution.BACKGROUND,
                TypeExecution.PARALLEL,
            ],
        )

        self.cmd_start.set_defaults(exec=StartCommand)

    def setup_schedule(self):
        self.cmd_schedule = self.subparsers.add_parser(
            "schedule", help="Schedule a workflow with a cron expression"
        )
        self.cmd_schedule = self.cmd_schedule.add_argument_group(
            "Usage: dotflow schedule [OPTIONS]"
        )

        self.cmd_schedule.add_argument("-s", "--step", required=True)
        self.cmd_schedule.add_argument(
            "--cron",
            required=True,
            help="Cron expression (e.g. '*/5 * * * *')",
        )
        self.cmd_schedule.add_argument(
            "-c", "--callback", default=basic_callback
        )
        self.cmd_schedule.add_argument("-i", "--initial-context")
        self.cmd_schedule.add_argument(
            "-o",
            "--storage",
            choices=[
                TypeStorage.DEFAULT,
                TypeStorage.FILE,
                TypeStorage.S3,
                TypeStorage.GCS,
            ],
        )
        self.cmd_schedule.add_argument(
            "-p", "--path", default=settings.START_PATH
        )
        self.cmd_schedule.add_argument(
            "-m",
            "--mode",
            default=TypeExecution.SEQUENTIAL,
            choices=[
                TypeExecution.SEQUENTIAL,
                TypeExecution.BACKGROUND,
                TypeExecution.PARALLEL,
            ],
        )
        self.cmd_schedule.add_argument(
            "--resume",
            action="store_true",
            default=False,
            help="Enable checkpoint-based resume",
        )
        self.cmd_schedule.add_argument(
            "--overlap",
            default=TypeOverlap.SKIP,
            choices=[
                TypeOverlap.SKIP,
                TypeOverlap.QUEUE,
                TypeOverlap.PARALLEL,
            ],
            help="Overlap strategy: skip, queue, or parallel",
        )

        self.cmd_schedule.set_defaults(exec=ScheduleCommand)

    def setup_cloud(self):
        self.cmd_cloud = self.subparsers.add_parser(
            "cloud",
            help="Generate cloud infrastructure files for a target platform",
        )
        cloud_subparsers = self.cmd_cloud.add_subparsers()

        cmd_generate = cloud_subparsers.add_parser(
            "generate", help="Generate infrastructure files"
        )
        cmd_generate.add_argument(
            "--platform",
            required=True,
            help="Target platform (e.g. docker, lambda, cloud-run, ecs, kubernetes)",
        )
        cmd_generate.add_argument(
            "--project",
            default=None,
            help="Project name (defaults to current directory name)",
        )
        cmd_generate.add_argument(
            "--output",
            default=".",
            help="Output directory (defaults to current directory)",
        )
        cmd_generate.set_defaults(exec=CloudGenerateCommand)

        cmd_list = cloud_subparsers.add_parser(
            "list", help="List available cloud platforms"
        )
        cmd_list.set_defaults(exec=CloudListCommand)

    def setup_logs(self):
        self.cmd_logs = self.subparsers.add_parser("logs", help="Logs")
        self.cmd_logs = self.cmd_logs.add_argument_group(
            "Usage: dotflow log [OPTIONS]"
        )
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
