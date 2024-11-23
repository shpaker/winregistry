from __future__ import annotations

import winreg
from abc import ABC, abstractmethod
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Generator, Iterator

if TYPE_CHECKING:
    from types import TracebackType

__all__ = [
    'Key',
    'KeyInfo',
    'Value',
    'ValueInfo',
    'open_key',
    'open_value',
    'robot',
]
__title__ = 'winregistry'
__version__ = '0.0.0'
__url__ = 'https://github.com/shpaker/winregistry'
__author__ = 'Aleksandr Shpak'
__author_email__ = 'shpaker@gmail.com'
__license__ = 'MIT'

_REG_KEYS_MAPPING: dict[str, int] = {
    value: name
    for name, values in {
        winreg.HKEY_CLASSES_ROOT: ('HKCR', 'HKEY_CLASSES_ROOT'),
        winreg.HKEY_CURRENT_USER: ('HKCU', 'HKEY_CURRENT_USER'),
        winreg.HKEY_LOCAL_MACHINE: ('HKLM', 'HKEY_LOCAL_MACHINE'),
        winreg.HKEY_USERS: ('HKU', 'HKEY_USERS'),
        winreg.HKEY_PERFORMANCE_DATA: ('HKPD', 'HKEY_PERFORMANCE_DATA'),
        winreg.HKEY_CURRENT_CONFIG: ('HKCC', 'HKEY_CURRENT_CONFIG'),
        winreg.HKEY_DYN_DATA: ('HKDD', 'HKEY_DYN_DATA'),
    }.items()
    for value in values
}
_REG_TYPES_MAPPING: dict[str, int] = {
    'BINARY': winreg.REG_BINARY,
    'DWORD': winreg.REG_DWORD,
    'DWORD_LITTLE_ENDIAN': winreg.REG_DWORD_LITTLE_ENDIAN,
    'DWORD_BIG_ENDIAN': winreg.REG_DWORD_BIG_ENDIAN,
    'EXPAND_SZ': winreg.REG_EXPAND_SZ,
    'LINK': winreg.REG_LINK,
    'MULTI_SZ': winreg.REG_MULTI_SZ,
    'NONE': winreg.REG_NONE,
    'QWORD': winreg.REG_QWORD,
    'QWORD_LITTLE_ENDIAN': winreg.REG_QWORD_LITTLE_ENDIAN,
    'RESOURCE_LIST': winreg.REG_RESOURCE_LIST,
    'FULL_RESOURCE_DESCRIPTOR': winreg.REG_FULL_RESOURCE_DESCRIPTOR,
    'RESOURCE_REQUIREMENTS_LIST': winreg.REG_RESOURCE_REQUIREMENTS_LIST,
    'SZ': winreg.REG_SZ,
}

KeyInfo = namedtuple(
    'KeyInfo', ['child_keys_count', 'values_count', 'modified_at']
)
ValueInfo = namedtuple('RawValueInfo', ['data', 'type'])


class RegEntity(
    ABC,
):
    def __init__(
        self,
        key: winreg.HKEYType,
        auto_refresh: bool,
    ) -> None:
        self._hkey = key
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
    ) -> Any:
        if not self._info:
            self.refresh()
        return self._info


class Value(
    RegEntity,
):
    def __init__(
        self,
        key: winreg.HKEYType,
        name: str,
        auto_refresh: bool = True,
    ) -> None:
        self._name = name
        super().__init__(
            key=key,
            auto_refresh=auto_refresh,
        )

    @classmethod
    def from_index(
        cls,
        key: winreg.HKEYType,
        index: int,
    ) -> Value:
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
            ),
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
    def __init__(
        self,
        key: winreg.HKEYType,
        auto_refresh: bool = True,
    ) -> None:
        super().__init__(
            key=key,
            auto_refresh=auto_refresh,
        )

    def refresh(
        self,
    ) -> None:
        self._info = KeyInfo(
            *winreg.QueryInfoKey(
                self._hkey,
            ),
        )

    @classmethod
    def from_index(
        cls,
        key: winreg.HKEYType,
        index: int,
    ) -> Key:
        sub_key = winreg.EnumKey(key, index)
        return Key(
            winreg.OpenKey(
                key=key,
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
        return datetime(1601, 1, 1) + timedelta(
            microseconds=self.info.modified_at / 10
        )

    @property
    def child_keys_names(
        self,
    ):
        for index in range(self.child_keys_count):
            yield winreg.EnumKey(self._hkey, index)

    @property
    def child_keys(
        self,
    ) -> Iterator[Key]:
        for index in range(self.child_keys_count):
            yield self.from_index(
                key=self._hkey,
                index=index,
            )

    @property
    def values(
        self,
    ) -> Iterator[Value]:
        for index in range(self.values_count):
            yield Value.from_index(self._hkey, index)

    def open_key(
        self,
        sub_key: str,
        access: int = winreg.KEY_READ,
        auto_refresh: bool = True,
    ) -> Key:
        """
        Opens the specified key
        """
        if access != winreg.KEY_READ and self._is_auto_refreshable:
            access = access | winreg.KEY_READ
        return Key(
            winreg.OpenKey(
                key=self._hkey,
                sub_key=sub_key,
                reserved=0,
                access=access,
            ),
            auto_refresh=auto_refresh,
        )

    def create_key(
        self,
        sub_key: str,
        access: int = winreg.KEY_READ,
        auto_refresh: bool = True,
    ) -> Key:
        """
        Creates or opens the specified key
        """
        if access != winreg.KEY_READ and self._is_auto_refreshable:
            access = access | winreg.KEY_READ
        key = Key(
            winreg.CreateKeyEx(
                key=self._hkey,
                sub_key=sub_key,
                reserved=0,
                access=access,
            ),
            auto_refresh=auto_refresh,
        )
        self._auto_refresh()
        return key

    def delete_key(
        self,
        sub_key: str,
        recursive: bool = False,
    ) -> None:
        """
        Deletes the specified key
        """
        if recursive:
            with self.open_key(
                sub_key,
                access=winreg.KEY_WRITE | winreg.KEY_READ,
                auto_refresh=False,
            ) as key:
                for entity in key.child_keys_names:
                    key.delete_key(
                        entity,
                        recursive=True,
                    )
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
            key=self._hkey,
            name=name,
        )

    def set_value(
        self,
        name: str,
        type: int | str,  # noqa: A002
        data: Any = None,
    ) -> None:
        """
        Associates a value with a specified key
        """
        if isinstance(type, str):
            type = _REG_TYPES_MAPPING[type]  # noqa: A001
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
    ) -> Key:
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
        return _REG_KEYS_MAPPING[key], sub_key
    key_root, key_subkey = key.split('\\', maxsplit=1)
    key = _REG_KEYS_MAPPING[key_root]
    sub_key = key_subkey if sub_key is None else f'{key_subkey}\\{sub_key}'
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
    if sub_key_access != winreg.KEY_READ and auto_refresh:
        sub_key_access = sub_key_access | winreg.KEY_READ
    if isinstance(key, str):
        key, sub_key = _make_int_key(key, sub_key)
    with Key(
        key=winreg.ConnectRegistry(computer_name, key),
        auto_refresh=auto_refresh,
    ) as reg:
        if not sub_key:
            yield reg
            return
        try:
            with reg.open_key(
                sub_key,
                access=sub_key_access,
                auto_refresh=auto_refresh,
            ) as _key:
                yield _key
        except OSError:
            if not sub_key_ensure:
                raise
        else:
            return
        with reg.create_key(
            sub_key,
            access=sub_key_access,
            auto_refresh=auto_refresh,
        ) as _key:
            yield _key


@contextmanager
def open_value(
    key_name: str,
    value_name: Any,
    computer_name: str | None = None,
    auto_refresh: bool = True,
    sub_key_access: int = winreg.KEY_READ,
) -> Generator[Value, None, None]:
    if sub_key_access != winreg.KEY_READ and auto_refresh:
        sub_key_access = sub_key_access | winreg.KEY_READ
    with open_key(
        key_name,
        computer_name=computer_name,
        auto_refresh=auto_refresh,
        sub_key_access=sub_key_access,
    ) as client:
        yield client.read_value(name=value_name)


class robot:  # noqa: N801
    @staticmethod
    def registry_key_should_exist(
        key_name: str,
    ) -> None:
        with open_key(
            key_name,
            sub_key_ensure=False,
            auto_refresh=False,
        ) as _:
            return

    @classmethod
    def registry_key_should_not_exist(
        cls,
        key_name: str,
    ) -> None:
        try:
            cls.registry_key_should_exist(key_name)
        except FileNotFoundError:
            return
        raise FileExistsError

    @staticmethod
    def registry_value_should_exist(
        key_name: str,
        value_name: str,
    ) -> None:
        with open_value(
            key_name,
            value_name=value_name,
            auto_refresh=False,
        ) as _:
            return

    @classmethod
    def registry_value_should_not_exist(
        cls,
        key_name: str,
        value_name: str,
    ) -> None:
        try:
            cls.registry_value_should_exist(key_name, value_name)
        except FileNotFoundError:
            return
        raise FileExistsError

    @staticmethod
    def create_registry_key(
        key_name: str,
    ) -> None:
        sub_key_name = None
        if '\\' in key_name:
            key_name, sub_key_name = key_name.split('\\', maxsplit=1)
        if sub_key_name and '\\' in sub_key_name:
            sub_key_name, new_key_name = sub_key_name.rsplit('\\', maxsplit=1)
        with open_key(
            key_name,
            sub_key=sub_key_name,
            sub_key_ensure=True,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as client:
            client.create_key(new_key_name)

    @staticmethod
    def delete_registry_key(
        key_name: str,
        recursive: bool = False,
    ) -> None:
        key_name, sub_key_name = key_name.rsplit('\\', maxsplit=1)
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as client:
            client.delete_key(sub_key_name, recursive=recursive)

    @staticmethod
    def get_registry_key_sub_keys(
        key_name: str,
    ) -> list[str]:
        with open_key(
            key_name,
            auto_refresh=False,
        ) as key:
            key.refresh()
            return list(key.child_keys_names)

    @staticmethod
    def get_registry_key_values_names(
        key_name: str,
    ) -> list[str]:
        with open_key(
            key_name,
            auto_refresh=False,
        ) as client:
            return [value.name for value in client.values]

    @staticmethod
    def read_registry_value(
        key_name: str,
        value_name: Any,
    ) -> Value:
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as client:
            return client.read_value(name=value_name)

    @staticmethod
    def create_registry_value(
        key_name: str,
        value_name: str,
        type: str,  # noqa: A002
        data: Any = None,
    ) -> None:
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as key:
            key.set_value(name=value_name, type=type, data=data)

    @staticmethod
    def set_registry_value(
        key_name: str,
        value_name: str,
        data: Any,
    ) -> None:
        with open_value(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            value_name=value_name,
            auto_refresh=False,
        ) as value:
            value.data = data

    @staticmethod
    def delete_registry_value(
        key_name: str,
        value_name: str,
    ) -> None:
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as key:
            key.delete_value(value_name)
