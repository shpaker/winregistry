import winreg
from typing import Tuple

from winregistry._types import ShortRootAlias
from winregistry._errors import KeyNotFoundError
import contextlib


def expand_short_root(
    root: str,
) -> str:
    with contextlib.suppress(KeyError):
        root = ShortRootAlias[root].value
    return root


def get_access_key(
    access: int,
    key_wow64_32key: bool = False,
) -> int:
    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    return access | x64_key


def parse_path(
    path: str,
) -> Tuple[winreg.HKEYType, str]:
    _root, key_path = path.split("\\", maxsplit=1)
    _root = expand_short_root(_root.upper())
    reg_root = getattr(winreg, _root)
    if not key_path:
        raise KeyNotFoundError(path)
    return reg_root, key_path
