import winreg
from enum import Enum, IntEnum, unique
from typing import Tuple
from winreg import KEY_WOW64_32KEY, KEY_WOW64_64KEY, HKEYType


@unique
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


def expand_short_root(
    root: str,
) -> str:
    try:
        root = ShortRootAlias[root].value
    except KeyError:
        pass
    return root


def get_access_key(
    access: int,
    key_wow64_32key: bool = False,
) -> int:
    x64_key = KEY_WOW64_32KEY if key_wow64_32key else KEY_WOW64_64KEY
    return access | x64_key


def parse_path(
    path: str,
) -> Tuple[HKEYType, str]:
    _root, key_path = path.split("\\", maxsplit=1)
    _root = expand_short_root(_root.upper())
    reg_root = getattr(winreg, _root)
    if not key_path:
        raise ValueError('Not found key in "{}"'.format(path))
    return reg_root, key_path
