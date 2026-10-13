"""Command flow module"""

from dotflow.cli.command import Command
from dotflow.core.module import Module
from dotflow.utils.visualizer import visualize


class FlowCommand(Command):
    def setup(self):
        step = self.params.step
        mode = self.params.mode
        fmt = self.params.format

        loaded = Module(value=step)
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
        if hasattr(obj, "task") and hasattr(obj.task, "queue"):
            return list(obj.task.queue)

        if hasattr(obj, "queue"):
            return list(obj.queue)

        if isinstance(obj, list):
            return obj

        return []
