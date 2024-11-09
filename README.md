# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

Python library aimed at working with Windows Registry 

## Installation

```bash
pip install winregistry
```

## Usage

```py
import winreg
from winregistry import connect_registry

_SUB_KEY_NAME = "SOFTWARE\_REMOVE_ME_"

if __name__ == "__main__":
  with connect_registry(winreg.HKEY_LOCAL_MACHINE) as hklm:
    hklm.create_key(_SUB_KEY_NAME)
    with hklm.open_key(_SUB_KEY_NAME) as subkey:
      subkey.set_value("remove_me", winreg.REG_SZ, "Don't forget remove me!")
      value = subkey.read_value("remove_me")
      print(f"{value=}: {value.data}")
      value.data = "remove me again!"
      print(f"{value=}: {value.data}")
      print(f"{list(subkey.values)=}")
      subkey.delete_value("remove_me")
      print(f"{list(subkey.values)=}")
      hklm.delete_key(_SUB_KEY_NAME)
```
