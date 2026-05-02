"""Tests for the workflow visualizer."""

import unittest

from dotflow import DotFlow, action
from dotflow.utils.visualizer import (
    _build_box,
    _render_mermaid,
    _render_parallel,
    _render_sequential,
    _task_name,
)


def _make_tasks(*steps):
    wf = DotFlow()
    for step in steps:
        wf.task.add(step)
    return list(wf.task.queue)


@action
def step_a():
    pass


@action(retry=3)
def step_b():
    pass


@action(timeout=60)
def step_c():
    pass


class TestTaskName(unittest.TestCase):
    def test_direct_decorator(self):
        tasks = _make_tasks(step_a)
        self.assertEqual(_task_name(tasks[0]), "step_a")

    def test_parametrised_decorator(self):
        tasks = _make_tasks(step_b)
        self.assertEqual(_task_name(tasks[0]), "step_b")

    def test_timeout_decorator(self):
        tasks = _make_tasks(step_c)
        self.assertEqual(_task_name(tasks[0]), "step_c")


class TestBuildBox(unittest.TestCase):
    def test_box_has_top_and_bottom_border(self):
        tasks = _make_tasks(step_a)
        box = _build_box(tasks[0], width=18)
        self.assertTrue(box[0].startswith("┌"))
        self.assertTrue(box[-1].startswith("└"))

    def test_box_contains_task_name(self):
        tasks = _make_tasks(step_a)
        box = _build_box(tasks[0], width=18)
        full = "\n".join(box)
        self.assertIn("step_a", full)

    def test_box_shows_retry(self):
        tasks = _make_tasks(step_b)
        box = _build_box(tasks[0], width=18)
        full = "\n".join(box)
        self.assertIn("retry: 3", full)

    def test_box_shows_timeout(self):
        tasks = _make_tasks(step_c)
        box = _build_box(tasks[0], width=18)
        full = "\n".join(box)
        self.assertIn("timeout: 60s", full)


class TestRenderSequential(unittest.TestCase):
    def test_all_task_names_present(self):
        tasks = _make_tasks(step_a, step_b, step_c)
        output = _render_sequential(tasks)
        self.assertIn("step_a", output)
        self.assertIn("step_b", output)
        self.assertIn("step_c", output)

    def test_arrow_connector_present(self):
        tasks = _make_tasks(step_a, step_b)
        output = _render_sequential(tasks)
        self.assertIn("──▶", output)

    def test_single_task_no_arrow(self):
        tasks = _make_tasks(step_a)
        output = _render_sequential(tasks)
        self.assertNotIn("──▶", output)

    def test_empty_returns_fallback(self):
        output = _render_sequential([])
        self.assertEqual(output, "(no tasks)")


class TestRenderParallel(unittest.TestCase):
    def test_all_names_present(self):
        tasks = _make_tasks(step_a, step_b, step_c)
        output = _render_parallel(tasks)
        self.assertIn("step_a", output)
        self.assertIn("step_b", output)
        self.assertIn("step_c", output)

    def test_bracket_chars_present(self):
        tasks = _make_tasks(step_a, step_b)
        output = _render_parallel(tasks)
        self.assertIn("┌", output)
        self.assertIn("└", output)

    def test_empty_returns_fallback(self):
        output = _render_parallel([])
        self.assertEqual(output, "(no tasks)")


class TestRenderMermaid(unittest.TestCase):
    def test_sequential_chain(self):
        tasks = _make_tasks(step_a, step_b, step_c)
        output = _render_mermaid(tasks, mode="sequential")
        self.assertIn("graph LR", output)
        # Node IDs include positional suffix; display labels are the original names
        self.assertIn('"step_a"', output)
        self.assertIn('"step_b"', output)
        self.assertIn('"step_c"', output)
        # There should be two arrows: a→b and b→c
        self.assertEqual(output.count("-->"), 2)

    def test_parallel_uses_start_end(self):
        tasks = _make_tasks(step_a, step_b)
        output = _render_mermaid(tasks, mode="parallel")
        self.assertIn("START -->", output)
        self.assertIn("--> END", output)
        self.assertIn('"step_a"', output)
        self.assertIn('"step_b"', output)

    def test_duplicate_names_produce_distinct_nodes(self):
        # Two tasks wrapping the same function must not collapse into a self-loop
        tasks = _make_tasks(step_a, step_a)
        output = _render_mermaid(tasks, mode="sequential")
        arrow_lines = [
            line.strip() for line in output.splitlines() if "-->" in line
        ]
        self.assertEqual(len(arrow_lines), 1)
        parts = arrow_lines[0].split("-->")
        # The left and right node IDs must differ
        self.assertNotEqual(parts[0].strip(), parts[1].strip())
