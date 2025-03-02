"""Integrations Test"""

import unittest

from examples.simple_class_workflow import main as simple_class_workflow
from examples.simple_class_workflow import main as simple_function_workflow
from examples.step_class_result_context import main as step_class_result_context
from examples.step_class_result_storage import main as step_class_result_storage
from examples.step_class_result_task import main as step_class_result_task
from examples.step_function_result_context import main as step_function_result_context
from examples.step_function_result_storage import main as step_function_result_storage
from examples.step_function_result_task import main as step_function_result_task
from examples.workflow_keep_going_true import main as workflow_keep_going_true
from examples.workflow_previous_context import main as workflow_previous_context
from examples.workflow_retry import main as workflow_retry
from examples.workflow_step_callback import main as workflow_step_callback
from examples.workflow_with_callback_failure import main as workflow_with_callback_failure
from examples.workflow_with_callback_success import main as workflow_with_callback_success


class TestIntegration(unittest.TestCase):

    def test_simple_class_workflow(self):
        simple_class_workflow()

    def test_simple_function_workflow(self):
        simple_function_workflow()

    def test_step_class_result_context(self):
        step_class_result_context()

    def test_step_class_result_storage(self):
        step_class_result_storage()

    def test_step_class_result_task(self):
        step_class_result_task()

    def test_step_function_result_context(self):
        step_function_result_context()

    def test_step_function_result_storage(self):
        step_function_result_storage()

    def test_step_function_result_task(self):
        step_function_result_task()

    def test_workflow_keep_going_true(self):
        workflow_keep_going_true()

    def test_workflow_previous_context(self):
        workflow_previous_context()

    def test_workflow_retry(self):
        workflow_retry()

    def test_workflow_step_callback(self):
        workflow_step_callback()

    def test_workflow_with_callback_failure(self):
        workflow_with_callback_failure()

    def test_workflow_with_callback_success(self):
        workflow_with_callback_success()
