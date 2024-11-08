# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

Python package aimed at working with Windows Registry 

## Installation

Install via PyPI:

```bash
pip install winregistry
```

## Usage

```python
import winreg
from winregistry import connect_registry

# connect to registry
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
) as hklm:
    ...

# connect to registry and open sub-key
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE",
) as key:
    ...

# connect to registry and ensure sub-key
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE\_REMOVE_ME_",
    sub_key_ensure=True,
) as key:
    ...

# also you can connect to registry with string key
with connect_registry(
    "HKLM\SOFTWARE",
) as key:
    ...

# open key
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
) as hklm:
    with hklm.open_key("SOFTWARE"):
        ...

# create or open sub-key
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE",
) as key:
    with key.create_key("_REMOVE_ME_"):
        ...

# delete key
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE",
) as key:
    key.delete_key("_REMOVE_ME_")

# set value to subkey
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE\_REMOVE_ME_",
    sub_key_ensure=True,
) as key:
    key.set_value(
        name="remove_me",
        type=winreg.REG_SZ,
        value="Remove me!",
    )

# read value
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE\_REMOVE_ME_",
    sub_key_ensure=True,
) as key:
    value = key.read_value("remove_me")

# change data of value
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE\_REMOVE_ME_",
    sub_key_ensure=True,
) as key:
    value.data = "Don't forget remove me!"

# delete value in subkey
with connect_registry(
    winreg.HKEY_LOCAL_MACHINE,
    sub_key="SOFTWARE\_REMOVE_ME_",
    sub_key_ensure=True,
) as key:
    value = key.delete_value("remove_me")

```
