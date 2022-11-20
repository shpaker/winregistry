# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

Minimalist Python library aimed at working with Windows Registry.

## Installation

```bash
pip install winregistry
```

## Usage

```py
from winregistry import WinRegistry

TEST_REG_PATH = r"HKLM\SOFTWARE\_REMOVE_ME_"


if __name__ == "__main__":
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
        Write Registry Entry    ${path}             Notepad   notepad.exe
        ${autorun} =            Read Registry Key   ${path}
        Delete Registry Entry   ${path}             Notepad
```
