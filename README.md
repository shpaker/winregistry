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

_SUB_KEY_NAME = "SOFTWARE\_REMOVE_ME_"


# connect to registry
with connect_registry(winreg.HKEY_LOCAL_MACHINE) as hklm:
  
  # create registry key
  hklm.create_key(_SUB_KEY_NAME)
  
  # open registry subkey
  with hklm.open_key(_SUB_KEY_NAME) as subkey:
    
    # set value to subkey
    subkey.set_value("remove_me", winreg.REG_SZ, "Remove me!")
    
    # read value
    value = subkey.read_value("remove_me")
    
    # change data of value
    value.data = "Don't forget remove me!"
    
    # delete value in subkey
    hklm.delete_key(_SUB_KEY_NAME)
```
