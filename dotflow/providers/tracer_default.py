"""Tracer Default"""

from typing import Any

from dotflow.abc.tracer import Tracer


class TracerDefault(Tracer):

    def start_workflow(self, workflow_id: Any, **kwargs) -> None:
        pass

    def end_workflow(self, workflow_id: Any, **kwargs) -> None:
        pass

    def start_task(self, task: Any) -> None:
        pass

    def end_task(self, task: Any) -> None:
        pass
