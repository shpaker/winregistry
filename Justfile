SOURCE_FILE := "winregistry.py"
TESTS_FILE := "winregistry_tests.robot"

tests: robot
fmt: black isort

isort:
  poetry run isort {{ SOURCE_FILE }}

black:
  poetry run black {{ SOURCE_FILE }}

pytest:
  poetry run pytest -vv

ruff:
  poetry run ruff check --fix {{ SOURCE_FILE }}

mypy:
  poetry run mypy --pretty {{ SOURCE_FILE }}

robot:
  poetry run robot {{ TESTS_FILE }}
