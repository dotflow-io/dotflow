import unittest

from dotflow.providers.server_default import ServerDefault


class TestServerDefault(unittest.TestCase):
    def test_instantiation(self):
        server = ServerDefault()
        self.assertIsInstance(server, ServerDefault)

    def test_create_workflow_noop(self):
        server = ServerDefault()
        server.create_workflow(workflow="wf-1")

    def test_update_workflow_noop(self):
        server = ServerDefault()
        server.update_workflow(workflow="wf-1", status="Completed")

    def test_create_task_noop(self):
        server = ServerDefault()
        server.create_task(task=None)

    def test_update_task_noop(self):
        server = ServerDefault()
        server.update_task(task=None)
