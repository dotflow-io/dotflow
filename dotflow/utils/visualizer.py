"""Workflow visualizer — terminal and Mermaid rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.text import Text

if TYPE_CHECKING:
    from dotflow.core.task import Task

console = Console()

# ── Box-drawing constants ─────────────────────────────────────────────────────

_TL = "┌"
_TR = "┐"
_BL = "└"
_BR = "┘"
_H = "─"
_V = "│"
_ARR = "──▶"
_FORK = "┬"
_JOIN_TOP = "┐"
_JOIN_BOT = "┘"
_BRANCH_TOP = "┌"
_BRANCH_BOT = "└"


def _task_name(task: Task) -> str:
    step = task.step

    func = getattr(step, "func", None)
    if func is not None:
        return getattr(func, "__name__", None) or type(func).__name__

    # @action(retry=N) wraps the original function in a closure.
    # We must introspect __closure__ to recover the original function name
    # because the wrapper doesn't preserve __name__.
    if callable(step) and getattr(step, "__closure__", None):
        free_vars = step.__code__.co_freevars
        cells = step.__closure__
        if "args" in free_vars:
            args_cell = cells[free_vars.index("args")].cell_contents
            if args_cell:
                return (
                    getattr(args_cell[0], "__name__", None)
                    or type(args_cell[0]).__name__
                )

    return getattr(step, "__name__", None) or type(step).__name__


def _action_instance(task: Task):
    """Return the Action instance for a task regardless of decoration style."""
    step = task.step
    if hasattr(step, "retry"):
        return step
    if callable(step) and getattr(step, "__closure__", None):
        free_vars = step.__code__.co_freevars
        if "self" in free_vars:
            return step.__closure__[free_vars.index("self")].cell_contents
    return None


def _task_config(task: Task) -> list[str]:
    """Return notable config lines for the box body (retry, timeout)."""
    lines = []
    action = _action_instance(task)
    if action is None:
        return lines
    if getattr(action, "retry", 1) != 1:
        lines.append(f"retry: {action.retry}")
    if getattr(action, "timeout", 0):
        lines.append(f"timeout: {action.timeout}s")
    return lines


def _task_status(task: Task) -> str | None:
    """Return a status line if the task has already been executed."""
    from dotflow.core.types.status import TypeStatus

    status = getattr(task, "_status", None)
    if status is None or status == TypeStatus.NOT_STARTED:
        return None

    symbol = TypeStatus.get_symbol(status) or ""
    duration = getattr(task, "_duration", None)
    dur_str = f" {duration:.2f}s" if duration is not None else ""
    errors = getattr(task, "_errors", None) or []
    err_str = ""
    if errors:
        last = errors[-1]
        exc = getattr(last, "exception", None)
        if exc:
            err_str = f"\n{exc}"
    return f"{symbol}{dur_str}{err_str}".strip()


# ── Box builder ───────────────────────────────────────────────────────────────


def _build_box(task: Task, width: int = 16) -> list[str]:
    """Return a list of strings representing a single task box."""
    name = _task_name(task)
    config_lines = _task_config(task)
    status_line = _task_status(task)

    inner = width - 2

    def pad(text: str) -> str:
        text = text[:inner]
        return f"{_V} {text:<{inner - 1}}{_V}"

    top = _TL + _H * (width - 2) + _TR
    bot = _BL + _H * (width - 2) + _BR

    rows = [top, pad(name)]

    if config_lines:
        rows.append(pad(""))
        for line in config_lines:
            rows.append(pad(line))

    if status_line:
        for line in status_line.splitlines():
            rows.append(pad(line))

    rows.append(bot)
    return rows


# ── Sequential renderer ───────────────────────────────────────────────────────


def _render_sequential(tasks: list[Task]) -> str:
    if not tasks:
        return "(no tasks)"

    box_w = 18
    connector = f" {_ARR} "
    boxes = [_build_box(t, width=box_w) for t in tasks]
    height = max(len(b) for b in boxes)

    # Pad all boxes to same height (insert blank lines before bottom border)
    padded = []
    for box in boxes:
        if len(box) < height:
            inner_w = box_w - 2
            filler = f"{_V} {' ' * (inner_w - 1)}{_V}"
            box = box[:-1] + [filler] * (height - len(box)) + [box[-1]]
        padded.append(box)

    mid = 1
    lines = []
    for row in range(height):
        parts = []
        for i, box in enumerate(padded):
            parts.append(box[row])
            if i < len(padded) - 1:
                parts.append(connector if row == mid else " " * len(connector))
        lines.append("".join(parts))

    return "\n".join(lines)


# ── Parallel renderer ─────────────────────────────────────────────────────────


def _render_parallel(tasks: list[Task]) -> str:
    """
    Render parallel tasks as a fork/join diagram:

        ┌──────────┐     ┌────────────┐
        │ task_a   │─┬──▶│ parallel_1 │──┐
        └──────────┘ │   └────────────┘  │  ┌──────────┐
                     │   ┌────────────┐  ├─▶│  join?   │
                     └──▶│ parallel_2 │──┘  └──────────┘
                         └────────────┘
    For dotflow parallel mode all tasks run concurrently so we just
    show them stacked with a leading/trailing bracket.
    """
    if not tasks:
        return "(no tasks)"

    box_w = 18
    boxes = [_build_box(t, width=box_w) for t in tasks]
    box_h = max(len(b) for b in boxes)

    padded = []
    for box in boxes:
        if len(box) < box_h:
            inner_w = box_w - 2
            filler = f"{_V} {' ' * (inner_w - 1)}{_V}"
            box = box[:-1] + [filler] * (box_h - len(box)) + [box[-1]]
        padded.append(box)

    indent = "  "

    lines = []
    for t_idx, box in enumerate(padded):
        for b_row, b_line in enumerate(box):
            if len(tasks) == 1:
                bracket = "  "
            elif t_idx == 0 and b_row == box_h // 2:
                bracket = "┌─"
            elif t_idx == len(tasks) - 1 and b_row == box_h // 2:
                bracket = "└─"
            elif b_row == box_h // 2:
                bracket = "├─"
            elif (
                (t_idx == 0 and b_row > box_h // 2)
                or (t_idx == len(tasks) - 1 and b_row < box_h // 2)
                or t_idx > 0
            ):
                bracket = "│ "
            else:
                bracket = "  "

            lines.append(f"{indent}{bracket}{b_line}")

        if t_idx < len(tasks) - 1:
            lines.append(f"{indent}│ ")

    return "\n".join(lines)


# ── Group renderer ────────────────────────────────────────────────────────────


def _render_groups(groups: dict[str, list[Task]]) -> str:
    """Render sequential groups — each group runs in its own process."""
    sections = []
    for group_name, tasks in groups.items():
        header = f"  ── group: {group_name} ──"
        body = _render_sequential(tasks)
        indented = "\n".join("  " + line for line in body.splitlines())
        sections.append(f"{header}\n{indented}")
    return "\n\n".join(sections)


# ── Mermaid export ────────────────────────────────────────────────────────────


def _render_mermaid(tasks: list[Task], mode: str) -> str:
    lines = ["graph LR"]
    names = [_task_name(t) for t in tasks]
    # Use positional suffixes as node IDs to prevent Mermaid collapsing
    # duplicate function names into a single node (self-loop).
    node_ids = [f"{name}_{i}" for i, name in enumerate(names)]

    if mode == "parallel":
        lines.append("  START:::hidden")
        lines.append("  END:::hidden")
        for node_id, name in zip(node_ids, names):
            lines.append(f'  START --> {node_id}["{name}"]')
            lines.append(f'  {node_id}["{name}"] --> END')
        lines.append("  classDef hidden display:none")
    else:
        for i in range(len(node_ids) - 1):
            lines.append(
                f'  {node_ids[i]}["{names[i]}"] --> {node_ids[i + 1]}["{names[i + 1]}"]'
            )

    return "\n".join(lines)


# ── Public API ────────────────────────────────────────────────────────────────


def visualize(
    tasks: list[Task],
    mode: str = "sequential",
    fmt: str = "terminal",
) -> None:
    """
    Render a workflow pipeline to the terminal or as Mermaid markup.

    Args:
        tasks: The task list from a DotFlow / TaskBuilder instance.
        mode:  Execution mode string — 'sequential', 'parallel',
               'background', or 'sequential_group'.
        fmt:   Output format — 'terminal' (default) or 'mermaid'.
    """
    from dotflow.core.workflow import grouper

    if fmt == "mermaid":
        console.print(_render_mermaid(tasks, mode), highlight=False)
        return

    # ── Terminal output ───────────────────────────────────────────────────────
    has_groups = len(grouper(tasks)) > 1

    if mode == "parallel":
        diagram = _render_parallel(tasks)
        mode_label = "parallel"
    elif mode == "background":
        diagram = _render_sequential(tasks)
        mode_label = "background"
    elif has_groups or mode == "sequential_group":
        diagram = _render_groups(grouper(tasks))
        mode_label = "sequential_group"
    else:
        diagram = _render_sequential(tasks)
        mode_label = "sequential"

    task_count = len(tasks)
    header = Text()
    header.append("dotflow viz", style="bold cyan")
    header.append(
        f"  ·  {task_count} task{'s' if task_count != 1 else ''}", style="dim"
    )
    header.append("  ·  mode: ", style="dim")
    header.append(mode_label, style="bold yellow")

    console.print()
    console.print(header)
    console.print()
    console.print(diagram)
    console.print()
