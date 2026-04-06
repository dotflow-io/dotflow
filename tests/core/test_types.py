"""Test type classes"""

import unittest

from dotflow.core.types import TypeExecution, TypeOverlap, TypeStatus


class TestTypeOverlap(unittest.TestCase):
    def test_skip_value(self):
        self.assertEqual(TypeOverlap.SKIP, "skip")

    def test_queue_value(self):
        self.assertEqual(TypeOverlap.QUEUE, "queue")

    def test_parallel_value(self):
        self.assertEqual(TypeOverlap.PARALLEL, "parallel")


class TestTypeExecution(unittest.TestCase):
    def test_sequential_value(self):
        self.assertEqual(TypeExecution.SEQUENTIAL, "sequential")

    def test_background_value(self):
        self.assertEqual(TypeExecution.BACKGROUND, "background")

    def test_parallel_value(self):
        self.assertEqual(TypeExecution.PARALLEL, "parallel")


class TestTypeStatus(unittest.TestCase):
    def test_not_started_value(self):
        self.assertEqual(TypeStatus.NOT_STARTED, "Not started")

    def test_completed_value(self):
        self.assertEqual(TypeStatus.COMPLETED, "Completed")

    def test_failed_value(self):
        self.assertEqual(TypeStatus.FAILED, "Failed")
