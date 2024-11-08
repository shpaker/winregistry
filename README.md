# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

Python package aimed at working with Windows Registry 

## Installation

Install via PyPI:

```bash
pip install winregistry
```

## Advances usage

```python
import winreg
from winregistry import open_key, open_value

# connect to registry and ensure sub-key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\_REMOVE_ME_",
) as key:
  ...

# also you can connect to registry with string key
with open_key(
  "HKLM\SOFTWARE\_REMOVE_ME_",
) as key:
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
) as key:
  key.set_value(
    name="remove_me",
    type=winreg.REG_SZ,
    value="Remove me!",
  )

# create value
with open_key(
  "HKLM\SOFTWARE\_REMOVE_ME_", 
  sub_key_ensure=True, 
  sub_key_access=winreg.KEY_SET_VALUE,
) as key:
    key.set_value("foo", "SZ")

# read value
with open_value(
  "HKLM\SOFTWARE\_REMOVE_ME_", 
  value_name="remove_me",
) as value:
  ...
```

## Usage with [Robot Testing Framework](https://robotframework.org/)

### Documentation

https://shpaker.github.io/winregistry/winregistry.robot

### Example

```robotframework
*** Variables ***
${ SUITE_KEY_NAME }       HKLM\\SOFTWARE\\_ROBOT_TESTS_
${ SHORT_CASE_KEY_NAME }  _CASE_KEY_
${ CASE_KEY_NAME }        ${ SUITE_KEY_NAME }\\${ SHORT_CASE_KEY_NAME }
${ VALUE_NAME }           some_testing_value

*** Settings ***
Library         Collections
Library         winregistry.robot
Suite Setup     Create Registry Key  ${ SUITE_KEY_NAME }
Suite Teardown  Delete Registry Key  ${ SUITE_KEY_NAME }

*** Test Cases ***
TEST REGISTRY KEYS
    [Teardown]  Delete Registry Key     ${ CASE_KEY_NAME }

    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Not Contain Value   ${ items }  ${ SHORT_CASE_KEY_NAME }
    Registry Key Should Not Exist   ${ CASE_KEY_NAME }
    Create Registry Key             ${ CASE_KEY_NAME }
    Registry Key Should Exist       ${ CASE_KEY_NAME }
    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Contain Value       ${ items }  ${ SHORT_CASE_KEY_NAME }


TEST REGISTRY VALUES
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }

    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Not Contain Value           ${ items }          ${ VALUE_NAME }
    Registry Value Should Not Exist         ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Create Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }  SZ
    Registry Value Should Exist             ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Contain Value               ${ items }          ${ VALUE_NAME }
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     ${ EMPTY }
    Set Registry Value                      ${ CASE_KEY_NAME }  ${ VALUE_NAME }  Remove me!
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     Remove me!
    Delete Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }
```
