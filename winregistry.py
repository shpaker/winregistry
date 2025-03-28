"""
winregistry - A Python library for interacting with the Windows registry.

Author: Aleksandr Shpak
Email: shpaker@gmail.com
License: MIT
URL: https://github.com/shpaker/winregistry
"""

import winreg
from abc import ABC, abstractmethod
from collections import namedtuple
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta
from types import TracebackType
from typing import (
    Any,
    Literal,
    Self,
    TypedDict,
    TypeVar,
    Union,
)

# Type definitions
RegistryValueType = Literal[
    "BINARY",
    "DWORD",
    "DWORD_LITTLE_ENDIAN",
    "DWORD_BIG_ENDIAN",
    "EXPAND_SZ",
    "LINK",
    "MULTI_SZ",
    "NONE",
    "QWORD",
    "QWORD_LITTLE_ENDIAN",
    "RESOURCE_LIST",
    "FULL_RESOURCE_DESCRIPTOR",
    "RESOURCE_REQUIREMENTS_LIST",
    "SZ",
]

RegistryRootKey = Literal[
    "HKCR",
    "HKEY_CLASSES_ROOT",
    "HKCU",
    "HKEY_CURRENT_USER",
    "HKLM",
    "HKEY_LOCAL_MACHINE",
    "HKU",
    "HKEY_USERS",
    "HKPD",
    "HKEY_PERFORMANCE_DATA",
    "HKCC",
    "HKEY_CURRENT_CONFIG",
    "HKDD",
    "HKEY_DYN_DATA",
]

RegistryData = Union[str, int, bytes, list[str]]
T = TypeVar("T")


class RegistryValueData(TypedDict):
    data: RegistryData
    type: int


__all__ = [
    "Key",
    "KeyInfo",
    "Value",
    "ValueInfo",
    "open_key",
    "open_value",
    "robot",
]
__title__ = "winregistry"
__description__ = "A Python library for interacting with the Windows registry."
__version__ = "0.0.0"
__url__ = "https://github.com/shpaker/winregistry"
__author__ = "Aleksandr Shpak"
__author_email__ = "shpaker@gmail.com"
__license__ = "MIT"

_REG_KEYS_MAPPING: dict[str, int] = {
    value: name
    for name, values in {
        winreg.HKEY_CLASSES_ROOT: ("HKCR", "HKEY_CLASSES_ROOT"),
        winreg.HKEY_CURRENT_USER: ("HKCU", "HKEY_CURRENT_USER"),
        winreg.HKEY_LOCAL_MACHINE: ("HKLM", "HKEY_LOCAL_MACHINE"),
        winreg.HKEY_USERS: ("HKU", "HKEY_USERS"),
        winreg.HKEY_PERFORMANCE_DATA: ("HKPD", "HKEY_PERFORMANCE_DATA"),
        winreg.HKEY_CURRENT_CONFIG: ("HKCC", "HKEY_CURRENT_CONFIG"),
        winreg.HKEY_DYN_DATA: ("HKDD", "HKEY_DYN_DATA"),
    }.items()
    for value in values
}
_REG_TYPES_MAPPING: dict[str, int] = {
    "BINARY": winreg.REG_BINARY,
    "DWORD": winreg.REG_DWORD,
    "DWORD_LITTLE_ENDIAN": winreg.REG_DWORD_LITTLE_ENDIAN,
    "DWORD_BIG_ENDIAN": winreg.REG_DWORD_BIG_ENDIAN,
    "EXPAND_SZ": winreg.REG_EXPAND_SZ,
    "LINK": winreg.REG_LINK,
    "MULTI_SZ": winreg.REG_MULTI_SZ,
    "NONE": winreg.REG_NONE,
    "QWORD": winreg.REG_QWORD,
    "QWORD_LITTLE_ENDIAN": winreg.REG_QWORD_LITTLE_ENDIAN,
    "RESOURCE_LIST": winreg.REG_RESOURCE_LIST,
    "FULL_RESOURCE_DESCRIPTOR": winreg.REG_FULL_RESOURCE_DESCRIPTOR,
    "RESOURCE_REQUIREMENTS_LIST": winreg.REG_RESOURCE_REQUIREMENTS_LIST,
    "SZ": winreg.REG_SZ,
}

KeyInfo = namedtuple("KeyInfo", ["child_keys_count", "values_count", "modified_at"])
ValueInfo = namedtuple("RawValueInfo", ["data", "type"])


class RegEntity(
    ABC,
):
    """
    Abstract base class for registry entities.
    """

    def __init__(
        self,
        key: winreg.HKEYType,
        auto_refresh: bool,
    ) -> None:
        """
        Initializes a RegEntity instance.

        Args:
            key (winreg.HKEYType): The registry key handle.
            auto_refresh (bool): Whether to automatically refresh the entity info.
        """
        self._hkey = key
        self._info = None
        self._is_auto_refreshable = auto_refresh
        self._auto_refresh()

    @abstractmethod
    def refresh(
        self,
    ) -> None:
        """
        Refreshes the entity info.

        Example:
            entity.refresh()
        """
        raise NotImplementedError

    def _auto_refresh(
        self,
    ) -> None:
        """
        Automatically refreshes the entity info if auto_refresh is enabled.

        Example:
            entity._auto_refresh()
        """
        if self._is_auto_refreshable:
            self.refresh()

    @property
    def info(
        self,
    ) -> Any:
        """
        Retrieves the entity info.

        Returns:
            Any: The entity info.

        Example:
            info = entity.info
        """
        if not self._info:
            self.refresh()
        return self._info


class Value(
    RegEntity,
):
    """
    Represents a registry value.
    """

    def __init__(
        self,
        key: winreg.HKEYType,
        name: str,
        auto_refresh: bool = True,
    ) -> None:
        """
        Initializes a Value instance.

        Args:
            key (winreg.HKEYType): The registry key handle.
            name (str): The name of the registry value.
            auto_refresh (bool): Whether to automatically refresh the value info.
        """
        self._name: str = name
        super().__init__(
            key=key,
            auto_refresh=auto_refresh,
        )

    @classmethod
    def from_index(
        cls,
        key: winreg.HKEYType,
        index: int,
    ) -> Self:
        """
        Creates a Value instance from the specified index.

        Args:
            key (winreg.HKEYType): The registry key handle.
            index (int): The index of the value.

        Returns:
            Value: The created Value instance.

        Example:
            value = Value.from_index(key, index)
        """
        value_name, _, _ = winreg.EnumValue(key, index)
        return Value(
            key,
            name=value_name,
        )

    def refresh(
        self,
    ) -> None:
        """
        Refreshes the value info.

        Example:
            value.refresh()
        """
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
        """
        Retrieves the name of the registry value.

        Returns:
            str: The name of the registry value.

        Example:
            name = value.name
        """
        return self._name

    @property
    def data(
        self,
    ) -> RegistryData:
        """
        Retrieves the data of the registry value.

        Returns:
            RegistryData: The data of the registry value.

        Example:
            data = value.data
        """
        return self.info.data

    @data.setter
    def data(
        self,
        value: RegistryData,
    ) -> None:
        """
        Sets the data of the registry value.

        Args:
            value (RegistryData): The data to set.

        Example:
            value.data = new_data
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
        Retrieves the type of the registry value.

        Returns:
            int: The type of the registry value.

        Example:
            value_type = value.type
        """
        return self.info.type


class Key(
    RegEntity,
):
    """
    Represents a registry key.
    """

    def __init__(
        self,
        key: winreg.HKEYType,
        auto_refresh: bool = True,
    ) -> None:
        """
        Initializes a Key instance.

        Args:
            key (winreg.HKEYType): The registry key handle.
            auto_refresh (bool): Whether to automatically refresh the key info.
        """
        super().__init__(
            key=key,
            auto_refresh=auto_refresh,
        )

    def refresh(
        self,
    ) -> None:
        """
        Refreshes the key info.

        Example:
            key.refresh()
        """
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
    ) -> Self:
        """
        Creates a Key instance from the specified index.

        Args:
            key (winreg.HKEYType): The registry key handle.
            index (int): The index of the sub key.

        Returns:
            Key: The created Key instance.

        Example:
            sub_key = Key.from_index(key, index)
        """
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
        Retrieves the number of sub keys this key has.

        Returns:
            int: The number of sub keys.

        Example:
            count = key.child_keys_count
        """
        return self.info.child_keys_count

    @property
    def values_count(
        self,
    ) -> int:
        """
        Retrieves the number of values this key has.

        Returns:
            int: The number of values.

        Example:
            count = key.values_count
        """
        return self.info.values_count

    @property
    def modified_at(
        self,
    ) -> datetime:
        """
        Retrieves the last modified time of the key.

        Returns:
            datetime: The last modified time.

        Example:
            modified_time = key.modified_at
        """
        return datetime(1601, 1, 1) + timedelta(microseconds=self.info.modified_at / 10)

    @property
    def child_keys_names(
        self,
    ) -> Iterator[str]:
        """
        Retrieves the names of the sub keys.

        Returns:
            Iterator[str]: The names of the sub keys.

        Example:
            for name in key.child_keys_names:
                print(name)
        """
        for index in range(self.child_keys_count):
            yield winreg.EnumKey(self._hkey, index)

    @property
    def child_keys(
        self,
    ) -> Iterator[Self]:
        """
        Retrieves the sub keys.

        Returns:
            Iterator[Key]: The sub keys.

        Example:
            for sub_key in key.child_keys:
                print(sub_key)
        """
        for index in range(self.child_keys_count):
            yield self.from_index(
                key=self._hkey,
                index=index,
            )

    @property
    def values(
        self,
    ) -> Iterator[Value]:
        """
        Retrieves the values of the key.

        Returns:
            Iterator[Value]: The values of the key.

        Example:
            for value in key.values:
                print(value)
        """
        for index in range(self.values_count):
            yield Value.from_index(self._hkey, index)

    def open_key(
        self,
        sub_key: str,
        access: int = winreg.KEY_READ,
        auto_refresh: bool = True,
    ) -> Self:
        """
        Opens the specified sub key.

        Args:
            sub_key (str): The name of the sub key to open.
            access (int): The access rights for the key.
            auto_refresh (bool): Whether to automatically refresh the key info.

        Returns:
            Key: The opened sub key.

        Example:
            with key.open_key('MySubKey') as sub_key:
                print(sub_key.child_keys_count)
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
    ) -> Self:
        """
        Creates or opens the specified sub key.

        Args:
            sub_key (str): The name of the sub key to create.
            access (int): The access rights for the key.
            auto_refresh (bool): Whether to automatically refresh the key info.

        Returns:
            Key: The created or opened sub key.

        Example:
            with key.create_key('MyNewSubKey') as new_key:
                print(new_key.child_keys_count)
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
        Deletes the specified sub key.

        Args:
            sub_key (str): The name of the sub key to delete.
            recursive (bool): Whether to delete sub keys recursively.

        Example:
            key.delete_key('MySubKey', recursive=True)
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
        Retrieves data for a specified value name.

        Args:
            name (str): The name of the value to read.

        Returns:
            Value: The registry value.

        Example:
            value = key.read_value('MyValue')
            print(value.data)
        """
        return Value(
            key=self._hkey,
            name=name,
        )

    def set_value(
        self,
        name: str,
        type: int | RegistryValueType,
        data: RegistryData | None = None,
    ) -> None:
        """
        Associates a value with a specified key.

        Args:
            name (str): The name of the value to set.
            type (int | str): The type of the value.
            data (Any): The data to set.

        Example:
            key.set_value('MyValue', 'SZ', 'MyData')
        """
        if isinstance(type, str):
            type = _REG_TYPES_MAPPING[type]
        winreg.SetValueEx(self._hkey, name, 0, type, data)
        self._auto_refresh()

    def delete_value(
        self,
        name: str,
    ) -> None:
        """
        Removes a named value from a registry key.

        Args:
            name (str): The name of the value to delete.

        Example:
            key.delete_value('MyValue')
        """
        winreg.DeleteValue(self._hkey, name)
        self._auto_refresh()

    def close(
        self,
    ) -> None:
        """
        Closes a previously opened registry key.

        Example:
            key.close()
        """
        self._hkey.Close()

    def __enter__(
        self,
    ) -> Self:
        """
        Enters the runtime context related to this object.

        Returns:
            Key: The registry key.

        Example:
            with key as k:
                print(k.child_keys_count)
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exits the runtime context related to this object.

        Args:
            exc_type (type[BaseException] | None): The exception type.
            exc_value (BaseException | None): The exception value.
            traceback (TracebackType | None): The traceback object.

        Example:
            with key as k:
                pass
        """
        self.close()


def _make_int_key(
    key: str | RegistryRootKey,
    sub_key: str | None = None,
) -> tuple[int, str | None]:
    if "\\" not in key:
        return _REG_KEYS_MAPPING[key], sub_key
    key_root, key_subkey = key.split("\\", maxsplit=1)
    key = _REG_KEYS_MAPPING[key_root]
    sub_key = key_subkey if sub_key is None else f"{key_subkey}\\{sub_key}"
    return key, sub_key.strip("\\")


@contextmanager
def open_key(
    key: int | str | RegistryRootKey,
    sub_key: str | None = None,
    computer_name: str | None = None,
    auto_refresh: bool = True,
    sub_key_ensure: bool = False,
    sub_key_access: int = winreg.KEY_READ,
) -> Generator[Key, None, None]:
    """
    Establishes a connection with the registry.

    Args:
        key (int | str | RegistryRootKey): The root key or its string representation.
        sub_key (str | None): The sub key to open.
        computer_name (str | None): The name of the remote computer.
        auto_refresh (bool): Whether to automatically refresh the key info.
        sub_key_ensure (bool): Whether to ensure the sub key exists.
        sub_key_access (int): The access rights for the sub key.

    Yields:
        Key: The opened registry key.

    Example:
        with open_key('HKEY_CURRENT_USER\\Software') as key:
            print(key.child_keys_count)
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
    key_name: str | RegistryRootKey,
    value_name: str,
    computer_name: str | None = None,
    auto_refresh: bool = True,
    sub_key_access: int = winreg.KEY_READ,
) -> Generator[Value, None, None]:
    """
    Establishes a connection with the registry value.

    Args:
        key_name (str | RegistryRootKey): The name of the key.
        value_name (str): The name of the value.
        computer_name (str | None): The name of the remote computer.
        auto_refresh (bool): Whether to automatically refresh the value info.
        sub_key_access (int): The access rights for the sub key.

    Yields:
        Value: The opened registry value.

    Example:
        with open_value('HKEY_CURRENT_USER\\Software', 'MyValue') as value:
            print(value.data)
    """
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
    """
    A class containing static methods for registry operations.
    """

    @staticmethod
    def registry_key_should_exist(
        key_name: str,
    ) -> None:
        """
        Verifies that the specified registry key exists.

        Arguments:
            key_name: Name of the key to verify.

        Example:
            | Registry Key Should Exist | HKEY_CURRENT_USER\\Software\\MyKey |
        """
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
        """
        Verifies that the specified registry key does not exist.

        Arguments:
            key_name: Name of the key to verify.

        Example:
            | Registry Key Should Not Exist | HKEY_CURRENT_USER\\Software\\MyKey |
        """
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
        """
        Verifies that the specified registry value exists.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to verify.

        Example:
            | Registry Value Should Exist | HKEY_CURRENT_USER\\Software | MyValue |
        """
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
        """
        Verifies that the specified registry value does not exist.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to verify.

        Example:
            | Registry Value Should Not Exist | HKEY_CURRENT_USER\\Software | MyValue |
        """
        try:
            cls.registry_value_should_exist(key_name, value_name)
        except FileNotFoundError:
            return
        raise FileExistsError

    @staticmethod
    def create_registry_key(
        key_name: str,
    ) -> None:
        """
        Creates a registry key.

        Arguments:
            key_name: Name of the key to create.

        Example:
            | Create Registry Key | HKEY_CURRENT_USER\\Software\\MyNewKey |
        """
        sub_key_name = None
        if "\\" in key_name:
            key_name, sub_key_name = key_name.split("\\", maxsplit=1)
        if sub_key_name and "\\" in sub_key_name:
            sub_key_name, new_key_name = sub_key_name.rsplit("\\", maxsplit=1)
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
        """
        Deletes a registry key.

        Arguments:
            key_name: Name of the key to delete.
            recursive: Whether to delete sub keys recursively.

        Example:
            | Delete Registry Key | HKEY_CURRENT_USER\\Software\\MyKey | recursive=True |
        """
        key_name, sub_key_name = key_name.rsplit("\\", maxsplit=1)
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as client:
            client.delete_key(sub_key_name, recursive=recursive)

    @staticmethod
    def get_registry_key_sub_keys(
        key_name: str | RegistryRootKey,
    ) -> list[str]:
        """
        Gets a list of sub keys for the specified registry key.

        Arguments:
            key_name: Name of the key.

        Returns:
            List of sub key names.

        Example:
            | ${sub_keys}= | Get Registry Key Sub Keys | HKEY_CURRENT_USER\\Software |
            | Log | ${sub_keys} |
        """
        with open_key(
            key_name,
            auto_refresh=False,
        ) as key:
            key.refresh()
            return list(key.child_keys_names)

    @staticmethod
    def get_registry_key_values_names(
        key_name: str | RegistryRootKey,
    ) -> list[str]:
        """
        Gets a list of value names for the specified registry key.

        Arguments:
            key_name: Name of the key.

        Returns:
            List of value names.

        Example:
            | ${value_names}= | Get Registry Key Values Names | HKEY_CURRENT_USER\\Software |
            | Log | ${value_names} |
        """
        with open_key(
            key_name,
            auto_refresh=False,
        ) as client:
            return [value.name for value in client.values]

    @staticmethod
    def read_registry_value(
        key_name: str | RegistryRootKey,
        value_name: str,
    ) -> Value:
        """
        Reads a registry value.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to read.

        Returns:
            The registry value.

        Example:
            | ${value}= | Read Registry Value | HKEY_CURRENT_USER\\Software | MyValue |
            | Log | ${value.data} |
        """
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as client:
            return client.read_value(name=value_name)

    @staticmethod
    def create_registry_value(
        key_name: str | RegistryRootKey,
        value_name: str,
        type: RegistryValueType,
        data: RegistryData | None = None,
    ) -> None:
        """
        Creates a registry value.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to create.
            type: Type of the value.
            data: Data to set.

        Example:
            | Create Registry Value | HKEY_CURRENT_USER\\Software | MyValue | SZ | MyData |
        """
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as key:
            key.set_value(name=value_name, type=type, data=data)

    @staticmethod
    def set_registry_value(
        key_name: str | RegistryRootKey,
        value_name: str,
        data: RegistryData,
    ) -> None:
        """
        Sets a registry value.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to set.
            data: Data to set.

        Example:
            | Set Registry Value | HKEY_CURRENT_USER\\Software | MyValue | NewData |
        """
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
        """
        Deletes a registry value.

        Arguments:
            key_name: Name of the key.
            value_name: Name of the value to delete.

        Example:
            | Delete Registry Value | HKEY_CURRENT_USER\\Software | MyValue |
        """
        with open_key(
            key_name,
            sub_key_access=winreg.KEY_ALL_ACCESS,
            auto_refresh=False,
        ) as key:
            key.delete_value(value_name)
