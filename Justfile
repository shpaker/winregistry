SOURCE_DIR := "winregistry"

tests: pytest
fmt: black isort

isort:
  poetry run isort {{ SOURCE_DIR }} --diff
#  poetry run isort test_curlify3.py --diff

black:
  poetry run isort {{ SOURCE_DIR }}
#  poetry run isort test_curlify3.py

pytest:
  poetry run pytest -vv

ruff:
  poetry run ruff check --fix {{SOURCE_DIR}}

mypy:
  poetry run mypy --pretty -p {{SOURCE_DIR}}
