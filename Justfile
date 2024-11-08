SOURCE_DIR := "winregistry.py"

tests: pytest
fmt: black isort

isort:
  poetry run isort {{ SOURCE_DIR }}

black:
  poetry run black {{ SOURCE_DIR }}


pytest:
  poetry run pytest -vv

ruff:
  poetry run ruff check --fix {{SOURCE_DIR}}

mypy:
  poetry run mypy --pretty {{SOURCE_DIR}}
