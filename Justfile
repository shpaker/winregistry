SOURCE_FILE := "winregistry.py"
TESTS_FILE := "winregistry_tests.robot"

fmt:
    poetry run ruff format -v {{ SOURCE_FILE }}

lint:
    poetry run ruff check {{ SOURCE_FILE }}

fix:
    poetry run ruff check --fix --unsafe-fixes {{ SOURCE_FILE }}

tests:
    poetry run robot {{ TESTS_FILE }}
