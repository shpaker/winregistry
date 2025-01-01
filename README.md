# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

## Project Description

WinRegistry is a Python package designed to simplify interactions with the Windows Registry. It provides a high-level interface for common registry operations such as creating, reading, updating, and deleting registry keys and values. The package supports both direct registry access using `winreg` and string-based key paths for convenience. Additionally, WinRegistry integrates with the Robot Testing Framework, enabling automated registry manipulation in testing scenarios.

Key features of WinRegistry include:
- Easy-to-use context managers for registry key operations.
- Support for both `winreg` constants and string-based key paths.
- Methods for creating, reading, updating, and deleting registry values.
- Integration with the Robot Testing Framework for automated testing.

## Installation

Install via PyPI:

```bash
pip install winregistry
```

## Usage

### Creating and Deleting Registry Keys

```python
import winreg
from winregistry import open_key

# Create a registry key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE\\MyApp",
  sub_key_ensure=True,
  sub_key_access=winreg.KEY_WRITE
) as key:
  print("Registry key created")

# Delete a registry key
with open_key(
  winreg.HKEY_LOCAL_MACHINE,
  sub_key="SOFTWARE",
  sub_key_access=winreg.KEY_WRITE
) as key:
  key.delete_key("MyApp")
  print("Registry key deleted")
```

### Setting and Reading Registry Values

```python
from winregistry import open_key, open_value

# Set a registry value
with open_key(
  "HKLM\\SOFTWARE\\MyApp",
  sub_key_ensure=True,
  sub_key_access=winreg.KEY_SET_VALUE
) as key:
  key.set_value("MyValue", "Sample Data", winreg.REG_SZ)
  print("Registry value set")

# Read a registry value
with open_value(
  "HKLM\\SOFTWARE\\MyApp",
  value_name="MyValue"
) as value:
  print(f"Registry value: {value.data}")
```

### Enumerating Subkeys and Values

```python
from winregistry import open_key

# Enumerate subkeys
with open_key(
  "HKLM\\SOFTWARE",
  sub_key_access=winreg.KEY_READ
) as key:
  subkeys = key.enum_subkeys()
  print(f"Subkeys: {subkeys}")

# Enumerate values
with open_key(
  "HKLM\\SOFTWARE\\MyApp",
  sub_key_access=winreg.KEY_READ
) as key:
  values = key.enum_values()
  print(f"Values: {values}")
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
