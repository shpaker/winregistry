"""
     Class for working with Robot Testing Framework
"""
from typing import Any, Optional

from winregistry import WinRegistry
from winregistry.enums import RegEntry, RegKey
from winregistry.utils import WinregType


class Keywords:
    def __init__(
        self,
        host: Optional[str] = None,
    ) -> None:
        self.reg = WinRegistry(host)

    def read_registry_key(
        self,
        key: str,
        key_wow64_32key: bool = False,
    ) -> RegKey:
        """Reading registry key"""
        resp = self.reg.read_key(key, key_wow64_32key)
        return resp

    def create_registry_key(
        self,
        key: str,
        key_wow64_32key: bool = False,
    ) -> None:
        """Creating registry key"""
        self.reg.create_key(key, key_wow64_32key)

    def delete_registry_key(
        self,
        key: str,
        key_wow64_32key: bool = False,
    ) -> None:
        """Deleting registry key"""
        self.reg.delete_key(key, key_wow64_32key)

    def read_registry_entry(
        self,
        key: str,
        value: Any,
        key_wow64_32key: bool = False,
    ) -> RegEntry:
        """Reading value from registry"""
        return self.reg.read_entry(key, value, key_wow64_32key)

    def write_registry_entry(
        self,
        key: str,
        value: str,
        data: Any = None,
        reg_type: str = "REG_SZ",
        key_wow64_32key: bool = False,
    ) -> None:
        """Writing (or creating) data in value"""
        self.reg.write_entry(key, value, data, WinregType[reg_type], key_wow64_32key)

    def delete_registry_entry(
        self,
        key: str,
        value: str,
        key_wow64_32key: bool = False,
    ) -> None:
        """Deleting value from registry"""
        self.reg.delete_entry(key, value, key_wow64_32key)
