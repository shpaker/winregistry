from __future__ import annotations

import winreg

from abc import ABC, abstractmethod
from collections import namedtuple
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta
from types import TracebackType
from typing import Any

from typing_extensions import Self

__all__ = [
    'Key',
    'Value',
    'KeyInfo',
    'ValueInfo',
    'open_key',
    'read_value',
    'create_key',
    'delete_key',
    'read_value_data',
    'set_value',
    'delete_value',
]
__version__ = '0.0.0'

_STR_KEYS_MAPPING: dict[str, int] = {
    value: name
    for name, values in {
        winreg.HKEY_CLASSES_ROOT: ('HKCR', "HKEY_CLASSES_ROOT"),
        winreg.HKEY_CURRENT_USER: ('HKCU', "HKEY_CURRENT_USER"),
        winreg.HKEY_LOCAL_MACHINE: ('HKLM', "HKEY_LOCAL_MACHINE"),
        winreg.HKEY_USERS: ('HKU', "HKEY_USERS"),
        winreg.HKEY_CURRENT_CONFIG: ('HKCC', "HKEY_CURRENT_CONFIG"),
    }.items()
    for value in values
}

KeyInfo = namedtuple('KeyInfo', ['child_keys_count', 'values_count', 'modified_at'])
ValueInfo = namedtuple('RawValueInfo', ['data', 'type'])


class RegEntity(
    ABC,
):
    def __init__(
        self,
        hkey: winreg.HKEYType,
        auto_refresh: bool,
    ) -> None:
        self._hkey = hkey
        self._info = None
        self._is_auto_refreshable = auto_refresh
        self._auto_refresh()

    @abstractmethod
    def refresh(
        self,
    ) -> None:
        raise NotImplementedError

    def _auto_refresh(
        self,
    ) -> None:
        if self._is_auto_refreshable:
            self.refresh()

    @property
    def info(
        self,
    ) -> tuple[...]:
        if not self._info:
            self.refresh()
        return self._info


class Value(
    RegEntity,
):
    raw_info: ValueInfo

    def __init__(
        self,
        hkey: winreg.HKEYType,
        name: str,
        auto_refresh: bool = True,
    ) -> None:
        self._name = name
        super().__init__(
            hkey=hkey,
            auto_refresh=auto_refresh,
        )

    @classmethod
    def from_index(
        cls,
        key: winreg.HKEYType,
        index: int,
    ) -> Self:
        value_name, _, _ = winreg.EnumValue(key, index)
        return Value(
            key,
            name=value_name,
        )

    def refresh(
        self,
    ) -> None:
        self._info = ValueInfo(
            *winreg.QueryValueEx(
                self._hkey,
                self._name,
            )
        )

    @property
    def name(
        self,
    ) -> str:
        return self._name

    @property
    def data(
        self,
    ) -> Any:
        """
        The data of the registry value item
        """
        return self.info.data

    @data.setter
    def data(
        self,
        value: Any,
    ) -> None:
        """
        Stores data in the value field of an open registry key
        """
        winreg.SetValueEx(
            self._hkey,
            self._name,
            0,
            self.type,
            value,
        )
        self._auto_refresh()

    @property
    def type(
        self,
    ) -> int:
        """
        An integer giving the registry type for this value
        """
        return self.info.type


class Key(
    RegEntity,
):
    raw_info: KeyInfo

    def __init__(
        self,
        hkey: winreg.HKEYType,
        auto_refresh: bool = True,
    ) -> None:
        super().__init__(
            hkey=hkey,
            auto_refresh=auto_refresh,
        )

    def refresh(
        self,
    ) -> None:
        self._raw_info = KeyInfo(
            *winreg.QueryInfoKey(
                self._hkey,
            )
        )

    @classmethod
    def from_index(
        cls,
        hkey: winreg.HKEYType,
        index: int,
    ) -> Self:
        sub_key = winreg.EnumKey(hkey, index)
        return Key(
            winreg.OpenKey(
                key=hkey,
                sub_key=sub_key,
                reserved=0,
                access=winreg.KEY_READ,
            ),
        )

    @property
    def child_keys_count(
        self,
    ) -> int:
        """
        Number of sub keys this key has
        """
        return self.info.child_keys_count

    @property
    def values_count(
        self,
    ) -> int:
        """
        Number of values this key has
        """
        return self.info.values_count

    @property
    def modified_at(
        self,
    ) -> datetime:
        return datetime(1601, 1, 1) + timedelta(microseconds=self._raw_info.modified_at / 10)

    @property
    def child_keys_names(
        self,
    ):
        for index in range(self.child_keys_count):
            yield winreg.EnumKey(self._hkey, index)

    @property
    def child_keys(
        self,
    ) -> Iterator[Self]:
        for index in range(self.child_keys_count):
            yield self.from_index(
                hkey=self._hkey,
                index=index,
            )

    @property
    def values(
        self,
    ) -> Iterator[Value]:
        for index in range(0, self.values_count):
            yield Value.from_index(self._hkey, index)

    def open_key(
        self,
        sub_key: str,
        access: int = winreg.KEY_READ,
    ) -> Self:
        """
        Opens the specified key
        """
        return Key(
            winreg.OpenKey(
                key=self._hkey,
                sub_key=sub_key,
                reserved=0,
                access=access,
            ),
        )

    def create_key(
        self,
        sub_key: str,
        access: int = winreg.KEY_READ,
    ) -> Self:
        """
        Creates or opens the specified key
        """
        key = Key(
            winreg.CreateKeyEx(
                key=self._hkey,
                sub_key=sub_key,
                reserved=0,
                access=access,
            )
        )
        self._auto_refresh()
        return key

    def delete_key(
        self,
        sub_key: str,
    ) -> None:
        """
        Deletes the specified key
        """
        winreg.DeleteKey(self._hkey, sub_key)
        self._auto_refresh()

    def read_value(
        self,
        name: str,
    ) -> Value:
        """
        Retrieves data for a specified value name
        """
        return Value(
            hkey=self._hkey,
            name=name,
        )

    def set_value(
        self,
        name: str,
        type: int,
        data: Any = None,
    ) -> None:
        """
        Associates a value with a specified key
        """
        winreg.SetValueEx(self._hkey, name, 0, type, data)
        self._auto_refresh()

    def delete_value(
        self,
        name: str,
    ) -> None:
        """
        Removes a named value from a registry key
        """
        winreg.DeleteValue(self._hkey, name)
        self._auto_refresh()

    def close(
        self,
    ) -> None:
        """
        Closes a previously opened registry key
        """
        self._hkey.Close()

    def __enter__(
        self,
    ) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


def _make_int_key(
    key: str,
    sub_key: str | None = None,
) -> tuple[int, str | None]:
    if '\\' not in key:
        return _STR_KEYS_MAPPING[key], sub_key
    key_root, key_subkey = key.split("\\", maxsplit=1)
    key = _STR_KEYS_MAPPING[key_root]
    sub_key = key_subkey if sub_key is None else '\\'.join((key_subkey, sub_key))
    return key, sub_key.strip('\\')


@contextmanager
def open_key(
    key: int | str,
    sub_key: str | None = None,
    computer_name: str | None = None,
    auto_refresh: bool = True,
    sub_key_ensure: bool = False,
    sub_key_access: int = winreg.KEY_READ,
) -> Generator[Key, None, None]:
    """
    Establishes a connection with registry
    """
    if isinstance(key, str):
        key, sub_key = _make_int_key(key, sub_key)
    with Key(
        hkey=winreg.ConnectRegistry(computer_name, key),
        auto_refresh=auto_refresh,
    ) as reg:
        if not sub_key:
            yield reg
            return
        try:
            with reg.open_key(sub_key, access=sub_key_access) as _key:
                yield _key
        except OSError:
            if not sub_key_ensure:
                raise
        else:
            return
        with reg.create_key(sub_key, access=sub_key_access) as _key:
            yield _key


@contextmanager
def read_value(key_name: str, value_name: Any) -> Generator[Value, None, None]:
    with open_key(key_name, sub_key_access=winreg.KEY_ALL_ACCESS) as client:
        yield client.read_value(name=value_name)


def read_value_data(key_name: str, value_name: Any) -> Any:
    with open_key(key_name, sub_key_access=winreg.KEY_ALL_ACCESS) as client:
        value = client.read_value(name=value_name)
        return value.data


def create_key(key_name: str) -> None:
    key_name, sub_key_name = key_name.split('\\', maxsplit=1)
    with open_key(key_name, sub_key=sub_key_name, sub_key_ensure=True, sub_key_access=winreg.KEY_ALL_ACCESS) as client:
        client.create_key(sub_key_name)


def child_keys_names(key_name: str) -> None:
    with open_key(key_name) as client:
        yield from client.child_keys_names


def delete_key(key_name: str) -> None:
    key_name, sub_key_name = key_name.rsplit('\\', maxsplit=1)
    with open_key(key_name, sub_key_access=winreg.KEY_ALL_ACCESS) as client:
        client.delete_key(sub_key_name)


def set_value(key_name: str, value_name: str, type: int, data: Any = None) -> None:
    with open_key(key_name, sub_key_access=winreg.KEY_ALL_ACCESS) as key:
        key.set_value(name=value_name, type=type, data=data)


def values_names(key_name: str) -> None:
    with open_key(key_name) as client:
        for value in client.values:
            yield value.name


def delete_value(key_name: str, value_name: str) -> None:
    with open_key(key_name, sub_key_access=winreg.KEY_ALL_ACCESS) as key:
        key.delete_value(value_name)
