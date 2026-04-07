"""Command viz module"""

from dotflow.cli.command import Command
from dotflow.core.module import Module
from dotflow.utils.visualizer import visualize


class VizCommand(Command):
    def setup(self):
        step = self.params.step
        mode = self.params.mode
        fmt = self.params.format

        # Load the workflow step (same module-loading pattern as StartCommand)
        loaded = Module(value=step)

        # The step may be a DotFlow instance, a TaskBuilder, or a bare list of Tasks.
        tasks = self._extract_tasks(loaded)
        visualize(tasks=tasks, mode=mode, fmt=fmt)

    @staticmethod
    def _extract_tasks(obj) -> list:
        """
        Accept any of the three common ways a user might point us at tasks:
          1. A DotFlow instance          → obj.task.queue
          2. A TaskBuilder instance      → obj.queue
          3. A plain list[Task]          → obj
        """
        # DotFlow wraps a TaskBuilder under .task
        if hasattr(obj, "task") and hasattr(obj.task, "queue"):
            return list(obj.task.queue)

        # TaskBuilder exposes .queue directly
        if hasattr(obj, "queue"):
            return list(obj.queue)

        # Plain list
        if isinstance(obj, list):
            return obj

        return []
