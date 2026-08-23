"""Setup module"""

from rich import print  # type: ignore

from dotflow import __description__, __version__
from dotflow.cli.commands import (
    CloudGenerateCommand,
    CloudListCommand,
    DeployCommand,
    FlowCommand,
    InitCommand,
    LogCommand,
    LoginCommand,
    LogoutCommand,
    ScheduleCommand,
    StartCommand,
)
from dotflow.core.exception import (
    MESSAGE_UNKNOWN_ERROR,
    ExecutionModeNotExist,
    ImportModuleError,
    InvalidWorkflowFactory,
    MissingActionDecorator,
    WorkflowFlagConflict,
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
        self.setup_login()
        self.setup_logout()
        self.setup_start()
        self.setup_schedule()
        self.setup_cloud()
        self.setup_deploy()
        self.setup_flow()
        self.command()

    def setup_login(self):
        cmd = self.subparsers.add_parser(
            "login", help="Authenticate the CLI via browser"
        )
        cmd.set_defaults(exec=LoginCommand)

    def setup_logout(self):
        cmd = self.subparsers.add_parser(
            "logout", help="Remove saved CLI credentials"
        )
        cmd.set_defaults(exec=LogoutCommand)

    def setup_init(self):
        self.cmd_init = self.subparsers.add_parser(
            "init", help="Scaffold a new dotflow project"
        )
        self.cmd_init = self.cmd_init.add_argument_group(
            "Usage: dotflow init <project-name>"
        )
        self.cmd_init.set_defaults(exec=InitCommand)

    def setup_start(self):
        cmd_start_parser = self.subparsers.add_parser("start", help="Start")
        entry_group = cmd_start_parser.add_mutually_exclusive_group(
            required=True
        )
        entry_group.add_argument("-s", "--step")
        entry_group.add_argument("-w", "--workflow")

        self.cmd_start = cmd_start_parser.add_argument_group(
            "Usage: dotflow start [OPTIONS]"
        )
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
        self.cmd_start.add_argument(
            "--resume",
            action="store_true",
            default=False,
            help="Enable checkpoint-based resume",
        )

        cmd_start_parser.set_defaults(exec=StartCommand)

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
            help=("Target platform (e.g. docker, lambda, cloud-run)"),
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

    def setup_deploy(self):
        self.cmd_deploy = self.subparsers.add_parser(
            "deploy",
            help="Deploy pipeline to a cloud platform",
        )
        self.cmd_deploy.add_argument(
            "--platform",
            required=True,
            help="Target platform (e.g. lambda, ecs)",
        )
        self.cmd_deploy.add_argument(
            "--project",
            default=None,
            required=True,
            help="Project name",
        )
        self.cmd_deploy.add_argument(
            "--region",
            default=None,
            help="Cloud region (e.g. us-east-1 for AWS, us-central1 for GCP)",
        )
        self.cmd_deploy.add_argument(
            "--schedule",
            default=None,
            help="Cron expression (e.g. '*/5 * * * *')",
        )
        self.cmd_deploy.set_defaults(exec=DeployCommand)

    def setup_flow(self):
        self.cmd_flow = self.subparsers.add_parser(
            "flow",
            help="Visualize a workflow pipeline in the terminal",
        )
        self.cmd_flow = self.cmd_flow.add_argument_group(
            "Usage: dotflow flow [OPTIONS]"
        )

        self.cmd_flow.add_argument(
            "-s",
            "--step",
            required=True,
            help="Dotted path to a DotFlow instance, TaskBuilder, or task list",
        )
        self.cmd_flow.add_argument(
            "-m",
            "--mode",
            default=TypeExecution.SEQUENTIAL,
            choices=[
                TypeExecution.SEQUENTIAL,
                TypeExecution.BACKGROUND,
                TypeExecution.PARALLEL,
                "sequential_group",
            ],
            help="Execution mode to visualize (default: sequential)",
        )
        self.cmd_flow.add_argument(
            "--format",
            default="terminal",
            choices=["terminal", "mermaid"],
            help="Output format: terminal (default) or mermaid",
        )

        self.cmd_flow.set_defaults(exec=FlowCommand)

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

        except InvalidWorkflowFactory as err:
            print(settings.WARNING_ALERT, err)

        except WorkflowFlagConflict as err:
            print(settings.WARNING_ALERT, err)

        except KeyboardInterrupt:
            print("\n", settings.INFO_ALERT, "Aborted.")

        except Exception as err:
            logger.error(f"Internal problem: {str(err)}")
            print(settings.ERROR_ALERT, MESSAGE_UNKNOWN_ERROR)
