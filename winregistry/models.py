from dataclasses import dataclass
from datetime import datetime
from typing import Any

from winregistry.consts import WinregType


@dataclass(frozen=True)
class RegEntry:
    name: str
    reg_key: str
    value: Any
    type: WinregType
    host: str | None = None


@dataclass(frozen=True)
class RegKey:
    name: str
    reg_keys: list[str]
    entries: list[RegEntry]
    modify_at: datetime
