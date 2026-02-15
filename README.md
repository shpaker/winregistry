# WinRegistry

[![PyPI](https://img.shields.io/pypi/v/winregistry.svg)](https://pypi.python.org/pypi/winregistry)
[![PyPI](https://img.shields.io/pypi/dm/winregistry.svg)](https://pypi.python.org/pypi/winregistry)

A Python library for interacting with the Windows registry.

**Windows only.** This library depends on the standard library module `winreg`, which is available only on Windows. On Linux or macOS you will get `ModuleNotFoundError: No module named 'winreg'`; use Windows or guard usage with a platform check (e.g. `if sys.platform == "win32"`). This library provides a simple and intuitive API for performing common registry operations, making it easier to work with the Windows registry in Python applications and automated tests.

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
  "HKLM\\SOFTWARE\\MyApp",
  sub_key_ensure=True,
  sub_key_access=winreg.KEY_WRITE,
) as key:
  print("Registry key created")

# Delete a registry key
with open_key(
  "HKLM\\SOFTWARE",
  sub_key_access=winreg.KEY_WRITE,
) as key:
  key.delete_key("MyApp")
  print("Registry key deleted")
```

### Setting and Reading Registry Values

```python
import winreg
from winregistry import open_key, open_value

# Set a registry value
with open_key(
  "HKLM\\SOFTWARE\\MyApp",
  sub_key_ensure=True,
  sub_key_access=winreg.KEY_WRITE,
) as key:
  key.set_value(
    "MyValue",
    winreg.REG_SZ,
    "Sample Data",
  )
  print("Registry value set")

# Read a registry value
with open_value(
  "HKLM\\SOFTWARE\\MyApp",
  value_name="MyValue",
) as value:
  print(f"Registry value: {value.data}")
```

### Enumerating Subkeys and Values

```python
import winreg
from winregistry import open_key

# Enumerate subkeys
with open_key(
  "HKLM\\SOFTWARE",
  sub_key_access=winreg.KEY_READ,
) as key:
  subkeys = list(key.child_keys_names)
  print(f"Subkeys: {subkeys}")

# Enumerate values
with open_key(
  "HKLM\\SOFTWARE\\MyApp",
  sub_key_access=winreg.KEY_READ,
) as key:
  values = [(v.name, v.data) for v in key.values]
  print(f"Values: {values}")
```

## Usage with [Robot Testing Framework](https://robotframework.org/)

The library provides a Robot Framework library that makes it easy to work with the Windows registry in automated tests. The library is available as `winregistry.robot`.

### Documentation

For detailed documentation of the Robot Framework library, visit:

https://shpaker.github.io/winregistry/winregistry.robot.html

### Example Tests

A complete set of example tests demonstrating various registry operations can be found in the [winregistry_tests.robot](winregistry_tests.robot) file. These tests cover:

- Creating and deleting registry keys
- Working with nested registry keys
- Setting and reading registry values
- Verifying registry key and value existence
- Enumerating subkeys and values

## Contributing

Contributions are welcome!

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

### Setting Up the Development Environment

We use `uv` for dependency management and packaging. To set up your development environment, follow these steps:

1. Install `uv` if you haven't already:

    ```bash
    pip install uv
    ```

2. Install the project dependencies:

    ```bash
    uv sync --group dev
    ```

### Code Formatting and Linting

We use `ruff` for code formatting and linting. The following tasks are defined in the `Justfile` to help with these processes:

- **Format the code:**

    ```bash
    just fmt
    ```

- **Run the linter:**

    ```bash
    just lint
    ```

## License

This project is licensed under the MIT License.
