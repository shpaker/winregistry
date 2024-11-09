import winreg

from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime, timedelta
from types import TracebackType
from typing import Any, Self

RawKeyInfo = namedtuple('RawKeyInfo', ['child_keys_count', 'values_count', 'modified_at'])
RawValueInfo = namedtuple('RawValueInfo', ['data', 'type'])


class RegEntity(
    ABC,
):
    def __init__(
        self,
        hkey: winreg.HKEYType,
        auto_refresh: bool,
    ) -> None:
        self._hkey = hkey
        self._raw_info = None
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
    def raw_info(
        self,
    ) -> tuple:
        if not self._raw_info:
            self.refresh()
        return self._raw_info


class Value(
    RegEntity,
):
    raw_info: RawValueInfo

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
        self._raw_info = RawValueInfo(
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
        return self.raw_info.data

    @data.setter
    def data(
        self,
        value: Any,
    ) -> None:
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
        return self.raw_info.type


class Key(
    RegEntity,
):
    raw_info: RawKeyInfo

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
        self._raw_info = RawKeyInfo(
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
        return self.raw_info.child_keys_count

    @property
    def values_count(
        self,
    ) -> int:
        return self.raw_info.values_count

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
    ):
        for index in range(self.child_keys_count):
            yield self.from_index(
                hkey=self._hkey,
                index=index,
            )

    @property
    def values(
        self,
    ):
        for index in range(0, self.values_count):
            yield Value.from_index(self._hkey, index)

    def open_key(
        self,
        sub_key: str,
    ) -> Self:
        return Key(
            winreg.OpenKey(
                key=self._hkey,
                sub_key=sub_key,
                reserved=0,
                access=winreg.KEY_READ,
            ),
        )

    def create_key(
        self,
        sub_key: str,
    ) -> None:
        winreg.CreateKeyEx(
            key=self._hkey,
            sub_key=sub_key,
            reserved=0,
            access=winreg.KEY_CREATE_SUB_KEY,
        )
        self._auto_refresh()

    def delete_key(
        self,
        sub_key: str,
    ) -> None:
        winreg.DeleteKey(self._hkey, sub_key)
        self._auto_refresh()

    def read_value(
        self,
        name: str,
    ) -> Value:
        return Value(
            hkey=self._hkey,
            name=name,
        )

    def set_value(
        self,
        name: str,
        type: int,
        value: Any,
    ) -> None:
        winreg.SetValueEx(self._hkey, name, 0, type, value)
        self._auto_refresh()

    def delete_value(
        self,
        name: str,
    ) -> None:
        winreg.DeleteValue(self._hkey, name)
        self._auto_refresh()

    def close(
        self,
    ) -> None:
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


def connect_registry(
    key: int,
    computer_name: str | None = None,
    auto_refresh: bool = True,
) -> Key:
    return Key(
        hkey=winreg.ConnectRegistry(computer_name, key),
        auto_refresh=auto_refresh,
    )


__all__ = [
    'connect_registry',
    'Key',
    'Value',
    'RawKeyInfo',
    'RawValueInfo',
]
__version__ = '0.0.0'
