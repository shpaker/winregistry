from datetime import datetime, timedelta
from typing import Any, Optional, Union, Type

import winreg
from winregistry._types import WinregType
from winregistry._types import RegEntry, RegKey
from winregistry._utils import get_access_key, parse_path


class WinRegistry:
    def __init__(
        self,
        host: Optional[str] = None,
    ) -> None:
        self.host: Optional[str] = host
        self._client: Optional[winreg.HKEYType] = None
        self._handler = None
        self._root: Optional[winreg.HKEYType] = None

    def _get_handler(
        self,
        key: str,
        access: int,
        key_wow64_32key: bool,
    ) -> winreg.HKEYType:
        root, path = parse_path(key)
        access_key = get_access_key(access, key_wow64_32key)
        if not self._client or root != self._root:
            self._client = winreg.ConnectRegistry(self.host, root)
        return winreg.OpenKey(
            key=self._client,
            sub_key=path,
            reserved=0,
            access=access_key,
        )

    def close(self) -> None:
        if self._client:
            self._client.Close()

    def __enter__(self) -> "WinRegistry":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[Any] = None,
    ) -> None:
        self.close()
        if exc_value:
            raise

    def read_entry(
        self,
        reg_key: str,
        name: str,
        key_wow64_32key: bool = False,
    ) -> RegEntry:
        handle = self._get_handler(reg_key, winreg.KEY_READ, key_wow64_32key)
        raw_value, raw_type = winreg.QueryValueEx(handle, name)
        return RegEntry(
            reg_key=reg_key,
            name=name,
            value=raw_value,
            type=WinregType(raw_type),
            host=self.host,
        )

    def write_entry(
        self,
        reg_key: str,
        name: str,
        value: Any = None,
        reg_type: Union[WinregType, int] = WinregType.REG_SZ,
        key_wow64_32key: bool = False,
    ) -> None:
        if isinstance(reg_type, int):
            reg_type = WinregType(reg_type)
        handle = self._get_handler(reg_key, winreg.KEY_SET_VALUE, key_wow64_32key)
        winreg.SetValueEx(handle, name, 0, reg_type.value, value)

    def delete_entry(
        self,
        key: str,
        name: str,
        key_wow64_32key: bool = False,
    ) -> None:
        handle = self._get_handler(key, winreg.KEY_SET_VALUE, key_wow64_32key)
        winreg.DeleteValue(handle, name)

    def read_key(
        self,
        name: str,
        key_wow64_32key: bool = False,
    ) -> RegKey:
        handle = self._get_handler(name, winreg.KEY_READ, key_wow64_32key)
        keys_num, values_num, modify = winreg.QueryInfoKey(handle)
        modify_at = datetime(1601, 1, 1) + timedelta(microseconds=modify / 10)
        keys = []
        entries = []
        for key_i in range(0, keys_num):
            keys.append(winreg.EnumKey(handle, key_i))
        for key_i in range(0, values_num):
            entry_name, value, raw_type = winreg.EnumValue(handle, key_i)
            entries.append(
                RegEntry(
                    reg_key=name,
                    name=entry_name,
                    value=value,
                    type=WinregType(raw_type),
                    host=self.host,
                ),
            )
        return RegKey(
            name=name,
            reg_keys=keys,
            entries=entries,
            modify_at=modify_at,
        )

    def create_key(
        self,
        name: str,
        key_wow64_32key: bool = False,
    ) -> None:
        handler = None
        sub_keys = name.split("\\")
        i = 0
        while i < len(sub_keys) and not handler:
            try:
                current = "\\".join(sub_keys[: len(sub_keys) - i])
                handler = self._get_handler(current, winreg.KEY_WRITE, key_wow64_32key)
            except FileNotFoundError:
                i += 1
        before_index = len(sub_keys) - i
        tail = "\\".join(sub_keys[before_index:])
        winreg.CreateKeyEx(
            key=handler,
            sub_key=tail,
            reserved=0,
            access=get_access_key(winreg.KEY_WRITE),
        )

    def delete_key(
        self,
        name: str,
        key_wow64_32key: bool = False,
    ) -> None:
        parental, key_name = name.rsplit(sep="\\", maxsplit=1)
        handle = self._get_handler(parental, winreg.KEY_WRITE, key_wow64_32key)
        winreg.DeleteKey(handle, key_name)

    def delete_key_tree(
        self,
        name: str,
        key_wow64_32key: bool = False,
    ) -> None:
        handle = self._get_handler(name, winreg.KEY_READ, key_wow64_32key)
        keys_num, values_num, modify = winreg.QueryInfoKey(handle)
        for key_i in range(0, keys_num):
            key = winreg.EnumKey(handle, key_i)
            self.delete_key_tree(f"{name}\\{key}", key_wow64_32key)
        handle.Close()
        self.delete_key(name, key_wow64_32key)
