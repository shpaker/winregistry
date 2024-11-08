import contextlib
import winreg

from winreg import KEY_WOW64_32KEY, KEY_WOW64_64KEY, HKEYType

from winregistry import ShortRootAlias


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
    x64_key = KEY_WOW64_32KEY if key_wow64_32key else KEY_WOW64_64KEY
    return access | x64_key


def parse_path(
    path: str,
) -> tuple[HKEYType, str]:
    _root, key_path = path.split("\\", maxsplit=1)
    _root = expand_short_root(_root.upper())
    reg_root = getattr(winreg, _root)
    if not key_path:
        raise ValueError(f'Not found key in "{path}"')
    return reg_root, key_path
