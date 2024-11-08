from winregistry import create_key

# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

Python package aimed at working with Windows Registry 

## Installation

Install via PyPI:

```bash
pip install winregistry
```

## QuickStart

```python
import winreg
import winregistry

KEY_NAME_FOR_TESTING = 'HKLM\SOFTWARE\_REMOVE_ME_'

# create key
winregistry.create_key(KEY_NAME_FOR_TESTING)
winregistry.create_key(f'{KEY_NAME_FOR_TESTING}\some_subkey')
print(list(winregistry.child_keys_names(f'{KEY_NAME_FOR_TESTING}\_REMOVE_ME_')))

# manipulations with values
winregistry.values_names(KEY_NAME_FOR_TESTING)
winregistry.set_value(KEY_NAME_FOR_TESTING, 'smth', winreg.REG_SZ, 'some data')
winregistry.values_names(KEY_NAME_FOR_TESTING)
with winregistry.read_value(KEY_NAME_FOR_TESTING, 'smth') as value:
  value.data = 'updated data!'
print(winregistry.read_value_data(KEY_NAME_FOR_TESTING, 'smth'))
winregistry.delete_value(KEY_NAME_FOR_TESTING, 'smth')

# delete key
winregistry.delete_key(f'{KEY_NAME_FOR_TESTING}\some_subkey')
winregistry.delete_key(KEY_NAME_FOR_TESTING)
```

## Advances usage

```python
import winreg
from winregistry import open_key

# connect to registry
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
) as hklm:
  ...

# connect to registry and open sub-key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE",
) as key:
  ...

# connect to registry and ensure sub-key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\_REMOVE_ME_",
  sub_key_ensure=True,
) as key:
  ...

# also you can connect to registry with string key
with open_key(
  "HKLM\SOFTWARE",
) as key:
  ...

# open key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
) as hklm:
  with hklm.open_key("SOFTWARE"):
    ...

# create or open sub-key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE",
) as key:
  with key.create_key("_REMOVE_ME_"):
    ...

# delete key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE",
) as key:
  key.delete_key("_REMOVE_ME_")

# set value to subkey
with open_key(
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
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\_REMOVE_ME_",
  sub_key_ensure=True,
) as key:
  value = key.read_value("remove_me")

# change data of value
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\_REMOVE_ME_",
  sub_key_ensure=True,
) as key:
  value.data = "Don't forget remove me!"

# delete value in subkey
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\_REMOVE_ME_",
  sub_key_ensure=True,
) as key:
  value = key.delete_value("remove_me")
```
