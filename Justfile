SOURCE_DIR := "winregistry"
TESTS_DIR := "tests"

format: isort black
linters: mypy ruff bandit safety
security: bandit safety
tests: pytest

isort:
  poetry run isort {{ SOURCE_DIR }} --diff --color
  poetry run isort {{ TESTS_DIR }} --diff --color

black:
  poetry run black {{ SOURCE_DIR }} {{ TESTS_DIR }}

ruff:
  poetry run ruff check --fix --unsafe-fixes {{ SOURCE_DIR }}

mypy:
  poetry run mypy --pretty -p {{ SOURCE_DIR }}

bandit:
  poetry run bandit -r {{ SOURCE_DIR }}

safety:
  poetry run safety --disable-optional-telemetry-data check --file poetry.lock

pytest:
  poetry run pytest -vv
