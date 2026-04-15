"""Test context of workflow"""

import unittest
from unittest.mock import MagicMock

from dotflow.core.config import Config
from dotflow.core.context import Context
from dotflow.core.dotflow import DotFlow
from dotflow.core.task import Task, TaskBuilder
from dotflow.core.types.status import TypeStatus
from dotflow.core.workflow import Manager
from tests.mocks import action_step


class TestDotFlow(unittest.TestCase):
    def setUp(self):
        self.workflow = DotFlow()
        self.workflow.task.add(step=action_step)

    def test_instantiating_dotflow_class(self):
        self.assertIsInstance(self.workflow.task, TaskBuilder)
        self.assertIsInstance(self.workflow.start(), Manager)

    def test_result_task_with_start(self):
        self.workflow.start()
        result = self.workflow.result_task()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Task)
        self.assertEqual(result[0].status, TypeStatus.COMPLETED)

    def test_result_context_with_start(self):
        self.workflow.start()
        result = self.workflow.result_context()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Context)

    def test_result_storage_with_start(self):
        self.workflow.start()
        result = self.workflow.result_storage()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {"foo": "bar"})

    def test_result_task_without_start(self):
        result = self.workflow.result_task()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Task)
        self.assertEqual(result[0].status, TypeStatus.NOT_STARTED)

    def test_result_context_without_start(self):
        result = self.workflow.result_context()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Context)

    def test_result_storage_without_start(self):
        result = self.workflow.result_storage()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], None)

    def test_create_workflow_fires_when_id_auto_generated(self):
        from dotflow.providers.server_default import ServerDefault

        server = ServerDefault()
        server.create_workflow = MagicMock()
        config = Config(server=server)
        workflow = DotFlow(config=config)

        server.create_workflow.assert_called_once_with(workflow=workflow)

    def test_create_workflow_skipped_when_id_externally_provided(self):
        from dotflow.providers.server_default import ServerDefault

        server = ServerDefault()
        server.create_workflow = MagicMock()
        config = Config(server=server)
        workflow = DotFlow(config=config, workflow_id="external-id")

        server.create_workflow.assert_not_called()
        self.assertEqual(workflow.workflow_id, "external-id")

    def test_task_ids_are_unique_ulids(self):
        from dotflow.providers.server_default import ServerDefault

        server = ServerDefault()
        config = Config(server=server)
        workflow = DotFlow(config=config)
        workflow.task.add(step=action_step)
        workflow.task.add(step=action_step)

        ids = [t.task_id for t in workflow.task.queue]
        self.assertEqual(len(ids), 2)
        self.assertNotEqual(ids[0], ids[1])
        for tid in ids:
            self.assertIsInstance(tid, str)
            self.assertEqual(len(tid), 26)

    def test_default_name_is_hostname(self):
        import socket

        workflow = DotFlow()
        self.assertEqual(workflow.name, socket.gethostname())

    def test_explicit_name_overrides_hostname(self):
        workflow = DotFlow(name="pipeline-xyz")
        self.assertEqual(workflow.name, "pipeline-xyz")

    def test_start_is_idempotent_for_same_queue(self):
        first = self.workflow.start()
        second = self.workflow.start()
        self.assertIs(first, second)

    def test_start_runs_again_after_task_clear(self):
        first = self.workflow.start()
        self.workflow.task.clear()
        self.workflow.task.add(step=action_step)
        second = self.workflow.start()
        self.assertIsNot(first, second)
