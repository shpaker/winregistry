from winregistry._errors import WinRegistryError, KeyNotFoundError
from winregistry._types import RegEntry, RegKey, ShortRootAlias, WinregType
from winregistry._winregistry import WinRegistry

__version__ = "0.1.0"
__all__ = (
    # client
    "WinRegistry",
    # types
    "ShortRootAlias",
    "WinregType",
    "RegEntry",
    "RegKey",
    # errors
    "WinRegistryError",
    "KeyNotFoundError",
)
