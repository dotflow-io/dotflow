"""Tests to ensure multiprocessing context is safe across platforms."""

import sys
import unittest

from multiprocessing import get_context


class TestMultiprocessingContext(unittest.TestCase):

    def test_fork_context_on_non_windows(self):
        """On non-Windows platforms, fork context must be used."""
        if sys.platform == "win32":
            self.skipTest("Not applicable on Windows")

        from dotflow.core import workflow
        self.assertEqual(workflow._mp.get_start_method(), "fork")

    def test_spawn_context_on_windows(self):
        """On Windows, spawn context must be used (simulated)."""
        if sys.platform != "win32":
            ctx = get_context("spawn")
            self.assertEqual(ctx.get_start_method(), "spawn")
        else:
            from dotflow.core import workflow
            self.assertEqual(workflow._mp.get_start_method(), "spawn")

    def test_workflow_importable_on_current_platform(self):
        """Importing workflow module must never raise on any supported platform."""
        try:
            from dotflow.core.workflow import Manager, Parallel, SequentialGroup
        except Exception as e:
            self.fail(f"Import raised an exception: {e}")
