# Changelog

All notable changes to this project will be documented in this file.

## [2.1.5] - 2026-04-02

### Fixed

- `NameError` in `create_registry_key()` when key path has no nested subkeys
- `ValueError` in `delete_registry_key()` when called with root key path
- `ValueInfo` namedtuple internal name mismatch (`RawValueInfo` → `ValueInfo`)
- Deprecated `set-output` syntax replaced with `$GITHUB_OUTPUT` in `pypi.yml`
- Robot Framework libdoc: moved class docstring before `ROBOT_LIBRARY_DOC_FORMAT`

### Added

- `AGENTS.md` with project rules

## [2.1.4] - 2026-02-15

### Fixed

- Clear `ImportError` message when `winreg` module is missing (non-Windows platforms)
- Documented Windows-only requirement in README

## [2.1.3] - 2026-02-15

### Fixed

- Corrected README code examples
- Fixed CI workflow configurations (`doc.yml`, `robot.yml`)
- Improved Robot Framework keyword documentation

## [2.1.2] - 2025-10-09

### Added

- Python 3.14 support

## [2.1.1] - 2025-03-31

### Changed

- Migrated from Poetry to uv as package manager
- Removed generated HTML documentation from repository root
- Updated Robot Framework keyword docstrings
- Updated CI workflows to use uv
- Refactored tests

## [2.1.0] - 2025-01-01

### Added

- Comprehensive docstrings and type annotations for all public API
- Extended README with detailed usage examples

## [2.0.1] - 2024-11-23

### Added

- Recursive key deletion (`delete_key` with `recursive=True`)

## [2.0.0] - 2024-11-22

### Changed

- Complete rewrite as a single-file module (`winregistry.py`) replacing the package structure
- Replaced Poetry with Hatchling as build backend
- New context-manager-based API (`open_key`, `open_value`)
- New `Key` and `Value` classes with `RegEntity` base
- Robot Framework keywords moved to `winregistry.robot` class
- Added `Justfile` for task automation
- Added Robot Framework test suite (`winregistry_tests.robot`)
- Added GitHub Actions workflow for Robot tests and libdoc generation

### Removed

- Old package structure (`winregistry/` directory with multiple modules)
- `pre-commit` configuration
- `mypy` configuration
- `flake8` configuration (replaced by `ruff`)
- Unit tests (`tests/`) replaced by Robot Framework integration tests
