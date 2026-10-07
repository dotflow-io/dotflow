"""Event bus"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from dotflow.logging import logger

if TYPE_CHECKING:
    from dotflow.core.task import Task
    from dotflow.core.types.status import TypeStatus


@dataclass
class StatusChanged:
    """Emitted when a task transitions to a new status."""

    task: Task
    old: TypeStatus
    new: TypeStatus


class EventBus:
    """In-process pub/sub. Subscribers run in registration order."""

    def __init__(self) -> None:
        self._subs: list[Callable[[Any], None]] = []

    def subscribe(self, handler: Callable[[Any], None]) -> None:
        self._subs.append(handler)

    def emit(self, event: Any) -> None:
        for handler in self._subs:
            try:
                handler(event)
            except Exception:
                logger.exception("event handler failed")
