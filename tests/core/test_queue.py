"""Test queue of task"""

import unittest

from dotflow.core.task import Task, Queue, QueueGroup, TASK_GROUP_NAME

from tests.mocks import action_step, simple_callback


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        self.index = 0

    def test_instantiating_queue_class(self):
        expected_tasks = []
        queue = Queue()
        self.assertIsInstance(queue, Queue)
        self.assertListEqual(queue.tasks, expected_tasks)

    def test_queue_add(self):
        queue = Queue()
        queue.add(item=self.task)

        self.assertEqual(queue.tasks[self.index], self.task)

    def test_queue_remove(self):
        queue = Queue()
        queue.add(item=self.task)
        queue.remove()

        self.assertFalse(queue.tasks)

    def test_queue_size(self):
        expected_size = 1
        queue = Queue()
        queue.add(item=self.task)

        self.assertEqual(queue.size(), expected_size)

    def test_queue_reverse(self):
        expected_task = Task(
            task_id=1,
            step=action_step,
            callback=simple_callback
        )
        queue = Queue()
        queue.add(item=self.task)
        queue.add(item=expected_task)
        queue.reverse()

        self.assertEqual(queue.tasks[self.index], expected_task)

    def test_queue_clear(self):
        queue = Queue()
        queue.add(item=self.task)
        queue.clear()

        self.assertFalse(queue.tasks)

    def test_queue_get(self):
        queue = Queue()
        queue.add(item=self.task)

        self.assertListEqual(queue.get(), [self.task])


class TestQueueGroup(unittest.TestCase):

    def setUp(self):
        self.task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback
        )
        self.index = 0

    def test_instantiating_queue_group_class(self):
        expected_queue = {}
        queue_group = QueueGroup()

        self.assertIsInstance(queue_group, QueueGroup)
        self.assertDictEqual(queue_group.queue, expected_queue)

    def test_queue_group_add(self):
        queue_group = QueueGroup()

        queue_group.add(item=self.task)

        self.assertIsNotNone(queue_group.queue.get(TASK_GROUP_NAME))
        self.assertIsInstance(queue_group.queue.get(TASK_GROUP_NAME), Queue)
        self.assertEqual(queue_group.queue[TASK_GROUP_NAME].tasks[self.index], self.task)

    def test_queue_group_size(self):
        expected_size = 1
        queue = QueueGroup()

        queue.add(item=self.task)

        self.assertEqual(queue.size(), expected_size)

    def test_queue_group_count(self):
        expected_count = 2
        task = Task(
            task_id=0,
            step=action_step,
            callback=simple_callback,
            group_name="new_group"
        )
        queue = QueueGroup()
        queue.add(item=self.task)
        queue.add(item=task)

        self.assertEqual(queue.count(), expected_count)

    def test_queue_group_tasks(self):
        queue = QueueGroup()
        queue.add(item=self.task)

        self.assertIsNotNone(queue.tasks())
        self.assertListEqual(queue.tasks(), [self.task])
