"""Test context of workflow"""

import unittest

from dotflow.core.controller import Controller
from dotflow.core.task import TaskBuilder
from dotflow.core.workflow import DotFlow


class TestDotFlow(unittest.TestCase):

    def test_instantiating_class(self):
        workflow = DotFlow()

        self.assertIsInstance(workflow.task, TaskBuilder)
        self.assertIsInstance(workflow.start(), Controller)
