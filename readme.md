# winregistry

Minimalist Python library aimed at working with Windows Registry.

## Installation

```bash
pip install winregistry
```

## Usage

```py
from winregistry import WinRegistry
with WinRegistry() as client:
    client.create_key(TEST_REG_PATH)
    client.write_entry(TEST_REG_PATH, "remove_me", "test")
    test_entry = client.read_entry(TEST_REG_PATH, "remove_me")
    assert test_entry.value == "test"
    client.delete_entry(TEST_REG_PATH, "remove_me")
```

Usage with ``Robot Testing Framework`` Library
----------------------------------------------

```
*** Settings ***
Library    winregistry.robot

*** Test Cases ***
Valid Login
        ${path} =    Set Variable    HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run
        Write Registry Value    ${path}             Notepad   notepad.exe
        ${autorun} =            Read Registry Key   ${path}
        Delete Registry Value   ${path}             Notepad
```