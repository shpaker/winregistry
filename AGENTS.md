# AGENTS.md

## Project overview

`winregistry` is a single-file Python library (`winregistry.py`) that wraps the Windows `winreg` module with a Pythonic API. It also provides Robot Framework keywords via the `robot` class. The package is Windows-only.

## Tech stack

- Python 3.8+
- Linter/formatter: ruff
- Tests: Robot Framework (`winregistry_tests.robot`)
- Task runner: just (Justfile)
- Package manager: uv

## After every code change

Run the following commands and fix any issues before committing:

```sh
just fmt lint tests
```

- `just fmt` — format code with ruff
- `just lint` — lint with ruff (strict rule set, see `pyproject.toml`)
- `just tests` — run Robot Framework tests (requires Windows)

If tests cannot run (e.g. on macOS/Linux), at minimum run `just fmt lint`.

## Code style

- Single source file: all library code lives in `winregistry.py`
- Line length limit: 120 characters
- Use type annotations everywhere
- Follow existing patterns — do not introduce new abstractions without need
- Commit messages: conventional commits (`fix:`, `feat:`, `chore:`, etc.)
- CHANGELOG.md: update only for stable releases (no entries for alpha/pre-release versions)
