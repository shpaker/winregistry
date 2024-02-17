import winreg
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, List, Optional


class ShortRootAlias(Enum):
    HKCR = "HKEY_CLASSES_ROOT"
    HKCU = "HKEY_CURRENT_USER"
    HKLM = "HKEY_LOCAL_MACHINE"
    HKU = "HKEY_USERS"
    HKCC = "HKEY_CURRENT_CONFIG"


class WinregType(IntEnum):
    REG_NONE = winreg.REG_NONE
    REG_SZ = winreg.REG_SZ
    REG_EXPAND_SZ = winreg.REG_EXPAND_SZ
    REG_BINARY = winreg.REG_BINARY
    REG_DWORD = winreg.REG_DWORD
    REG_DWORD_LITTLE_ENDIAN = winreg.REG_DWORD_LITTLE_ENDIAN
    REG_DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    REG_LINK = winreg.REG_LINK
    REG_MULTI_SZ = winreg.REG_MULTI_SZ
    REG_RESOURCE_LIST = winreg.REG_RESOURCE_LIST
    REG_FULL_RESOURCE_DESCRIPTOR = winreg.REG_FULL_RESOURCE_DESCRIPTOR
    REG_RESOURCE_REQUIREMENTS_LIST = winreg.REG_RESOURCE_REQUIREMENTS_LIST
    REG_QWORD = winreg.REG_QWORD
    REG_QWORD_LITTLE_ENDIAN = winreg.REG_QWORD_LITTLE_ENDIAN


@dataclass(frozen=True)
class RegEntry:
    name: str
    reg_key: str
    value: Any
    type: WinregType
    host: Optional[str] = None


@dataclass(frozen=True)
class RegKey:
    name: str
    reg_keys: List[str]
    entries: List[RegEntry]
    modify_at: datetime