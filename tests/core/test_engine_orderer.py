"""Test execution orderer with prefix method names"""

import unittest
from uuid import uuid4

from dotflow.core.action import Action as action
from dotflow.core.context import Context
from dotflow.core.engine import TaskEngine
from dotflow.core.task import Task
from tests.mocks import action_step, simple_callback


@action
class StepWithPrefixMethods:
    @action
    def run():
        return {"method": "run"}

    @action
    def run_all():
        return {"method": "run_all"}

    @action
    def run_all_tasks():
        return {"method": "run_all_tasks"}


class TestExecutionOrderer(unittest.TestCase):
    def setUp(self):
        self.workflow_id = uuid4()
        self.task = Task(task_id="01ARZ3NDEKTSV4RRFFQ69G5FAV", step=action_step, callback=simple_callback)

    def _make_engine(self):
        engine = TaskEngine(
            task=self.task,
            workflow_id=self.workflow_id,
            previous_context=Context(),
        )
        with engine.start():
            engine.execute()
        return engine

    def test_prefix_methods_ordered_correctly(self):
        engine = self._make_engine()

        class_instance = StepWithPrefixMethods(task=engine.task).storage
        callable_list = [
            func
            for func in dir(class_instance)
            if engine._is_action(class_instance, func)
        ]

        result = engine._execution_orderer(
            callable_list=callable_list, class_instance=class_instance
        )

        method_names = [name for _, name in result]

        self.assertEqual(len(result), 3)
        self.assertIn("run", method_names)
        self.assertIn("run_all", method_names)
        self.assertIn("run_all_tasks", method_names)

    def test_prefix_methods_no_duplicates(self):
        engine = self._make_engine()

        class_instance = StepWithPrefixMethods(task=engine.task).storage
        callable_list = [
            func
            for func in dir(class_instance)
            if engine._is_action(class_instance, func)
        ]

        result = engine._execution_orderer(
            callable_list=callable_list, class_instance=class_instance
        )

        method_names = [name for _, name in result]

        self.assertEqual(len(method_names), len(set(method_names)))

    def test_prefix_methods_source_order(self):
        engine = self._make_engine()

        class_instance = StepWithPrefixMethods(task=engine.task).storage
        callable_list = [
            func
            for func in dir(class_instance)
            if engine._is_action(class_instance, func)
        ]

        result = engine._execution_orderer(
            callable_list=callable_list, class_instance=class_instance
        )

        method_names = [name for _, name in result]

        self.assertEqual(method_names, ["run", "run_all", "run_all_tasks"])
