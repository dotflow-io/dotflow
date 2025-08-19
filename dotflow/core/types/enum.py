"""Enum Type module"""

import sys

from enum import Enum


class StrEnumType(str, Enum):
    ...


if sys.version_info >= (3, 11):
    from enum import StrEnum as StrEnum
else:
    StrEnum = StrEnumType


__all__ = ["StrEnum"]
