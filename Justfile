SOURCE_FILE := "winregistry.py"
TESTS_FILE := "winregistry_tests.robot"

fmt:
    uv run ruff format -v {{ SOURCE_FILE }}

lint:
    uv run ruff check {{ SOURCE_FILE }}

fix:
    uv run ruff check --fix --unsafe-fixes {{ SOURCE_FILE }}

tests:
    uv run robot {{ TESTS_FILE }}

doc:
    uv run libdoc winregistry.robot _doc/winregistry.robot.html
