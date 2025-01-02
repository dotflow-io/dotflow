"""Workflow"""

import logging
import threading

from uuid import uuid4
from typing import List

from dotflow.core.workflow import (
    Context,
    Task,
    Workflow
)


def execution_default(*args, **kwargs):
    pass


class Response:

    FAILED = "Failed"
    COMPLETED = "Completed"

    def __init__(
        self,
        id: str,
        task: Task,
        previous_context: Context,
        current_context: Context = Context(),
        status: str = COMPLETED,
        error: Exception = None
    ) -> None:
        self.id = id
        self.task = task
        self.previous_context = previous_context
        self.current_context = current_context
        self.status = status
        self.error = error


class Executor:

    @classmethod
    def execution(
        cls,
        id: str,
        task: Task,
        previous_context: Context,
        max_retry: int,
        attempt: int = 0,
        error: Exception = None
    ) -> Context:
        try:
            current_context = task.run(previous_context=previous_context)
            return Response(
                id=id,
                task=task,
                previous_context=previous_context,
                current_context=current_context
            )
        except Exception as error:
            logging.error(
                msg=f" {task.__class__.__name__} - ID: {id} TaskID: {task.task_id}"
            )
            attempt += 1

            if max_retry > attempt:
                cls.execution(id, task, previous_context, max_retry, attempt)

            return Response(
                id=id,
                task=task,
                previous_context=previous_context,
                status=Response.FAILED,
                error=error
            )

    @classmethod
    def start(
            cls,
            workflow: Workflow,
            execute_on_success: object = execution_default,
            execute_on_failure: object = execution_default) -> List[Response]:
        result = []
        id = uuid4().hex
        registry = workflow.build()
        previous_context = Context()

        for task in registry.queu:
            content = cls.execution(
                id=id,
                task=task,
                previous_context=previous_context,
                max_retry=task.RETRY,
            )
            previous_context = content.current_context
            result.append(content)

            if not task.CONTINUE:
                if content.status == Response.FAILED:
                    break

        try:
            final_status = [flow.status for flow in result]
            if Response.FAILED in final_status:
                execute_on_failure()
            else:
                execute_on_success()
        except Exception as error:
            logging.error(msg=f"{error}")

        return result

    @classmethod
    def start_in_background(
            cls,
            workflow: Workflow,
            execute_on_success: object = execution_default,
            execute_on_failure: object = execution_default) -> None:
        th = threading.Thread(
            target=cls.start,
            args=[workflow, execute_on_success, execute_on_failure]
        )
        th.start()
